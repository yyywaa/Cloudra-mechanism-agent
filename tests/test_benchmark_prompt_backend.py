"""External prompt execution uses the real runtime without mechanism scoring."""

import pytest

from cloudra.benchmark.backend import RuntimeV2Backend
from cloudra.runtime_v2.persistence import RuntimeStore
from cloudra.runtime_v2.schemas import OrchestrationMode
from cloudra.runtime_v2.turn_pipeline import LLMResponse


class PromptProvider:
    def __init__(self, *, error=None):
        self.requests = []
        self.error = error

    async def complete(self, agent, messages, tools, **kwargs):
        self.requests.append(messages)
        if self.error is not None:
            raise self.error
        return LLMResponse(content="External calculation report", stop_requested=True)


@pytest.mark.parametrize("role", [None, "small_mol"])
def test_run_prompt_preserves_query_without_benchmark_policy_and_persists_result(tmp_path, role):
    provider = PromptProvider()
    store_path = tmp_path / "runtime" / "runtime-v2.db"
    backend = RuntimeV2Backend(llm=provider, start_scheduler=False,
        poll_interval_s=0.01, stuck_grace_s=2.0, store_path=store_path)
    query = "Calculate the water Raman spectrum with the originally specified method."
    arguments = dict(task_id="external_1", query=query, sandbox=tmp_path / "case")
    if role is not None:
        arguments["role"] = role

    result = backend.run_prompt(**arguments)

    core = backend.core_by_task("external_1")
    project = core.projects[result["project_id"]]
    agent = core.agents[result["session_id"]]
    assert project.workspace_dir == str((tmp_path / "case").resolve())
    assert project.settings.benchmark_task_id is None
    assert project.settings.method_policy is None
    assert agent.role_id == (role or "coordinator")
    assert agent.settings.orchestration_mode == OrchestrationMode.STANDARD
    assert agent.settings.clean_context and agent.settings.unattended
    assert any(message.get("content") == query for message in provider.requests[0])
    assert result == {"project_id": project.id, "session_id": agent.id,
        "state": "succeeded", "final_message": "External calculation report"}
    assert not (tmp_path / "case" / "mechanism_graph.json").exists()
    events = RuntimeStore(store_path).read_events(session_id=agent.id)
    assert any(event.type == "agent.message_emitted" and
        event.data.get("content") == "External calculation report" for event in events)


def test_run_prompt_reports_failed_runtime_instead_of_success(tmp_path):
    class PermanentProviderError(Exception):
        status_code = 400

    backend = RuntimeV2Backend(llm=PromptProvider(error=PermanentProviderError("fixture rejection")),
        start_scheduler=False, poll_interval_s=0.01, stuck_grace_s=2.0)

    result = backend.run_prompt(task_id="external_failed", query="Original external task",
        sandbox=tmp_path / "failed")

    assert result["state"] == "failed"
    assert backend.core_by_task("external_failed").agents[result["session_id"]].state.value == "failed"
    assert "score" not in result and "verified" not in result
