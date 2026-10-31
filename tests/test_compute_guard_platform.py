"""Cross-platform guard cancellation without POSIX process-group APIs."""
from __future__ import annotations

import asyncio
import os
from types import SimpleNamespace

import pytest

from cloudra.persistence.database import ComputeDB
from cloudra.services.compute_store import get_compute_job, insert_compute_job


@pytest.mark.asyncio
async def test_non_posix_guard_waits_for_exit_before_acknowledging_cancel(tmp_path, monkeypatch):
    from cloudra.runtime import monitor

    db = ComputeDB().init()
    inp = tmp_path / "synthetic.gjf"
    inp.write_text("synthetic")
    job_id = insert_compute_job(
        db, node_id="node-local", conversation_id="platform-test", session_id="s",
        path=str(inp), state="running", jobtype="gaussian", scheduler="local",
    )
    spawned = asyncio.Event()
    release = asyncio.Event()
    waited = asyncio.Event()
    proc = SimpleNamespace(pid=12345, returncode=None)

    async def wait():
        waited.set()
        await release.wait()
        proc.returncode = 0
        return 0

    proc.wait = wait

    async def spawn(*_args, **kwargs):
        assert "start_new_session" not in kwargs
        assert "preexec_fn" not in kwargs
        spawned.set()
        return proc

    monkeypatch.setattr(monitor, "is_posix", lambda: False)
    monkeypatch.delattr(os, "killpg", raising=False)
    monkeypatch.setattr(asyncio, "create_subprocess_exec", spawn)
    monkeypatch.setattr(monitor, "check_job_type", lambda *_: (True, ""))
    monkeypatch.setattr(monitor, "build_calculator_cmd", lambda *_a, **_k: (True, ["synthetic"], ""))
    monkeypatch.setattr(monitor, "_CANCEL_POLL_SECONDS", 0.01)
    monkeypatch.setenv("GAUSS_SCRDIR", str(tmp_path / "scratch"))
    guard = asyncio.create_task(monitor.run_guard(
        taskid=job_id, path=str(inp), conv_id="platform-test", parse_timeout=1,
        db_path=db.path, job_type="gaussian",
    ))
    try:
        await asyncio.wait_for(spawned.wait(), 2)
        def request_cancel():
            with db.connect() as con:
                con.execute("UPDATE compute_jobs SET state='cancel_requested' WHERE id=?", (job_id,))
                con.commit()
        await asyncio.to_thread(request_cancel)
        await asyncio.wait_for(waited.wait(), 2)
        await asyncio.sleep(0.05)
        assert not guard.done()
        assert (await asyncio.to_thread(get_compute_job, db, job_id))["state"] == "cancel_requested"
        assert list((tmp_path / "scratch").glob("cloudra_g16_*"))
        release.set()
        await asyncio.wait_for(guard, 2)
        assert (await asyncio.to_thread(get_compute_job, db, job_id))["state"] == "cancelled"
        assert not list((tmp_path / "scratch").glob("cloudra_g16_*"))
        assert not (tmp_path / f"state_{job_id}.json").exists()
    finally:
        release.set()
        guard.cancel()
        await asyncio.gather(guard, return_exceptions=True)


def test_monitor_import_does_not_require_posix_calculator_wrapper(monkeypatch):
    import importlib
    import sys

    from cloudra.runtime import monitor

    monkeypatch.setitem(sys.modules, "cloudra.runtime.calc_lock_wrapper", None)
    importlib.reload(monitor)
