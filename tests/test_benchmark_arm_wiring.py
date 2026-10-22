"""Branch-pinned benchmark wiring without model calls or compute processes."""
from __future__ import annotations

import asyncio
import socket

import pytest

from cloudra.benchmark import runner as benchmark_runner
from cloudra.benchmark.schema import GoldSpec, PromptSpec, SystemSpec, TaskSpec
from cloudra.runtime_v2.schemas import OrchestrationMode


@pytest.fixture(autouse=True)
def no_external_network(monkeypatch):
    """These regressions are local; no telemetry or remote models are permitted."""
    def forbidden(*args, **kwargs):
        raise AssertionError("network is forbidden in benchmark-arm regression tests")
    monkeypatch.setattr(socket.socket, "connect", forbidden)
    monkeypatch.setenv("OTEL_SDK_DISABLED", "true")
    monkeypatch.setenv("DO_NOT_TRACK", "1")
    monkeypatch.setenv("ANONYMIZED_TELEMETRY", "False")


def _task(mode, role="coordinator"):
    return TaskSpec(task_id="ARM_LOCAL", tier="easy",
        prompt=PromptSpec(query="local configuration probe", orchestration_mode=mode, role=role),
        system=SystemSpec(reactants=["C"]),
        gold=GoldSpec(mechanism_graph={
            "nodes": [{"id": "R", "role": "reactant", "smiles": ["C"]}], "edges": []}))


@pytest.mark.parametrize("task_mode", list(OrchestrationMode))
def test_arm_is_shared_by_project_provenance_and_scoring(tmp_path, task_mode):
    task = _task(task_mode)
    expected = benchmark_runner.ABLATION_ARM.value
    settings = benchmark_runner.task_project_settings(task)
    assert settings["orchestration_mode"] == expected
    assert settings["method_policy"] == task.method_policy.model_dump(mode="json")
    assert settings["defaults"] == {"yolo": True, "unattended": True, "clean_context": True}
    assert benchmark_runner.provenance_config("probe", [task])["orchestration_modes"] == {task.task_id: expected}
    config = benchmark_runner.provenance_config("probe", [task])
    assert config["experiment_arm"] == "benchmark/arm-guided-brief-errors"
    assert config["error_feedback"] == "brief"
    sandbox = tmp_path / "sandbox"
    sandbox.mkdir()
    runner = benchmark_runner.BenchmarkRunner(tmp_path / "bench")
    assert runner.score_sandbox(task, sandbox).orchestration_mode == expected
    assert task.prompt.orchestration_mode is task_mode


@pytest.mark.parametrize("task_mode", list(OrchestrationMode))
@pytest.mark.parametrize("role", ["coordinator", "small_mol"])
@pytest.mark.asyncio
async def test_cli_actual_spawn_uses_branch_arm(tmp_path, monkeypatch, task_mode, role):
    from cloudra.benchmark.backend import RuntimeV2Backend
    from cloudra.runtime_v2.agent_runner import AgentRunner
    from cloudra.runtime_v2.child_settings import resolve_child_settings

    # Keep actual project/spawn/setting resolution; prevent scheduling any model turn.
    monkeypatch.setattr(AgentRunner, "schedule", lambda self, session_id: None)
    observed = []
    backend = RuntimeV2Backend(start_scheduler=False)

    async def inspect_spawn(bus, agent):
        project = bus.core.require_project(agent.project_id)
        observed.append((project.settings.orchestration_mode, agent.settings.orchestration_mode))
        plan = resolve_child_settings(parent=agent, project=project, role=bus.core.roles.get("small_mol"))
        assert plan.patch.orchestration_mode is benchmark_runner.ABLATION_ARM

    monkeypatch.setattr(backend, "_wait_terminal", inspect_spawn)
    await backend._run_task(_task(task_mode, role), tmp_path / "sandbox")
    assert observed == [(benchmark_runner.ABLATION_ARM, benchmark_runner.ABLATION_ARM)]
    assert all(agent.settings.orchestration_mode is benchmark_runner.ABLATION_ARM
               for agent in backend.last_core.agents.values())


@pytest.mark.parametrize("task_mode", list(OrchestrationMode))
@pytest.mark.parametrize("role", ["coordinator", "small_mol"])
@pytest.mark.asyncio
async def test_web_actual_spawn_and_result_use_branch_arm(tmp_path, task_mode, role):
    from cloudra.benchmark.batch import BenchmarkService
    from cloudra.runtime_v2.commands import CommandBus
    from cloudra.runtime_v2.core import RuntimeCore

    task = _task(task_mode, role)
    task_dir = tmp_path / "tasks"
    task_dir.mkdir()
    (task_dir / "task.json").write_text(task.model_dump_json())
    core = RuntimeCore(strict_events=True)  # no runner or LLM is attached
    bus = CommandBus(core)
    service = BenchmarkService(core, bus, data_dir=tmp_path / "bench")
    await service.start(tasks_dirs=[str(task_dir)], only="", concurrency=1)
    batch = service._batch
    try:
        async def spawned():
            while not batch.task_states[0].agent_id:
                await asyncio.sleep(.01)
        await asyncio.wait_for(spawned(), timeout=5)
        state = batch.task_states[0]
        agent = core.require_agent(state.agent_id)
        project = core.require_project(state.project_id)
        assert project.settings.orchestration_mode is benchmark_runner.ABLATION_ARM
        assert agent.settings.orchestration_mode is benchmark_runner.ABLATION_ARM
        assert batch.config["orchestration_modes"] == {task.task_id: benchmark_runner.ABLATION_ARM.value}
        await core.agent_host.start_run(agent)
        await core.agent_host.finish_run(agent, outcome="succeeded")
        await asyncio.wait_for(batch._task, timeout=5)
        assert state.result.orchestration_mode == benchmark_runner.ABLATION_ARM.value
    finally:
        if not batch._task.done():
            await service.stop()
            await asyncio.wait_for(batch._task, timeout=5)


@pytest.mark.parametrize("task_mode", list(OrchestrationMode))
def test_cli_failure_and_cancellation_keep_arm(tmp_path, task_mode):
    import threading

    def fail(task, sandbox):
        raise RuntimeError("local test failure")
    task = _task(task_mode)
    stop = threading.Event()
    runner = benchmark_runner.BenchmarkRunner(tmp_path / "bench", backend=fail, stop_event=stop)
    assert runner._run_one_guarded(task).orchestration_mode == benchmark_runner.ABLATION_ARM.value
    stop.set()
    assert runner._run_one_guarded(task).orchestration_mode == benchmark_runner.ABLATION_ARM.value


@pytest.mark.asyncio
async def test_web_failure_and_cancellation_keep_arm(tmp_path):
    from cloudra.benchmark.batch import BenchmarkBatch
    from cloudra.runtime_v2.commands import CommandBus
    from cloudra.runtime_v2.core import RuntimeCore

    core = RuntimeCore(strict_events=True)
    task = _task(OrchestrationMode.STANDARD)
    batch = BenchmarkBatch(core, CommandBus(core), data_dir=tmp_path / "bench",
        tasks=[task], tasks_dirs=[], concurrency=1, stuck_grace_s=1, poll_interval_s=.01,
        emit=lambda *args: None)
    batch._runner = await asyncio.to_thread(benchmark_runner.BenchmarkRunner, tmp_path / "bench")
    assert batch._cancelled_result(task, tmp_path).orchestration_mode == benchmark_runner.ABLATION_ARM.value
    state = batch.task_states[0]
    await batch._mark_infra_failure(state, "local infrastructure probe")
    assert state.result.orchestration_mode == benchmark_runner.ABLATION_ARM.value


@pytest.mark.asyncio
async def test_web_watcher_failure_keeps_arm(tmp_path, monkeypatch):
    from cloudra.benchmark.batch import BenchmarkBatch
    from cloudra.benchmark.watch import RunWatcher
    from cloudra.runtime_v2.commands import CommandBus
    from cloudra.runtime_v2.core import RuntimeCore

    async def fail_watcher(self, core, agent, cancel):
        return "local watcher probe"
    monkeypatch.setattr(RunWatcher, "wait", fail_watcher)
    core = RuntimeCore(strict_events=True)
    task = _task(OrchestrationMode.STANDARD)
    batch = BenchmarkBatch(core, CommandBus(core), data_dir=tmp_path / "bench",
        tasks=[task], tasks_dirs=[], concurrency=1, stuck_grace_s=1, poll_interval_s=.01,
        emit=lambda *args: None)
    await batch.start()
    await asyncio.wait_for(batch._task, timeout=5)
    state = batch.task_states[0]
    assert state.status == "error"
    assert state.result.orchestration_mode == benchmark_runner.ABLATION_ARM.value
    assert any("local watcher probe" in note for note in state.result.notes)


@pytest.mark.parametrize("disposition", ["complete", "partial"])
@pytest.mark.asyncio
async def test_guided_keeps_complete_only_irc_gate(tmp_path, monkeypatch, disposition):
    from cloudra.dag.controller import DagController
    from cloudra.persistence.database import ConversationDB

    db = await asyncio.to_thread(lambda: ConversationDB("guided-partial", data_dir=tmp_path).init())
    controller = DagController(db, "s1", "dag_guided", conversation_id="guided-partial")
    await controller.initialize()
    calls = []
    def record_irc_check(graph, report):
        calls.append(disposition)
        return report.unresolved
    monkeypatch.setattr(controller, "_required_irc_gaps", record_irc_check)
    gate = await controller.audit_stop(disposition)
    assert calls == (["complete"] if disposition == "complete" else [])
    assert gate.action == ("continue_work" if disposition == "complete" else "wait_review")
