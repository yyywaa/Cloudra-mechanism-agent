"""Original Aitomia task bank, executed without Cloudra's mechanism scorer."""

from __future__ import annotations

import json
import shutil
import time
from pathlib import Path
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field


class Case(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    task_id: str
    source_task_id: str
    level: Literal["Low", "Medium", "High"]
    query: str
    provided_xyz: bool
    source_row: int
    notes: str = ""
    reported_success_rate: float | None = None
    reported_runs: int | None = None
    reported_tokens: int | None = None
    source_type: str = ""


class Catalog(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    source: dict[str, Any]
    cases: list[Case] = Field(min_length=1)


def load_catalog() -> Catalog:
    return Catalog.model_validate_json(Path(__file__).with_name("catalog.json").read_text(encoding="utf-8"))


def write_json(path: Path, value: Any) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def prepare_case(case: Case, workspace: Path, xyz: Path | None = None) -> dict:
    workspace = workspace.resolve()
    workspace.mkdir(parents=True, exist_ok=True)
    record = {
        "task_id": case.task_id,
        "workspace": str(workspace),
        "execution_status": "prepared",
        "scientific_status": "unreviewed",
        "score": None,
    }
    if case.provided_xyz and xyz is None:
        record.update(execution_status="blocked_input", reason="Original task requires an unpublished XYZ input.")
    else:
        query = case.query.replace("[working_dir]", str(workspace))
        if xyz is not None:
            target = workspace / "input.xyz"
            shutil.copyfile(xyz, target)
            if "[xyzfile]" in query:
                query = query.replace("[xyzfile]", str(target))
            else:
                query += f"\nInput geometry file: {target}"
        write_json(workspace / "request.json", {"task_id": case.task_id, "query": query})
    write_json(workspace / "result.json", record)
    return record


def execute_case(record: dict, backend: Any) -> dict:
    if record["execution_status"] == "blocked_input":
        return record
    workspace = Path(record["workspace"])
    request = json.loads((workspace / "request.json").read_text(encoding="utf-8"))
    started = time.monotonic()
    record = {**record, "execution_status": "running"}
    write_json(workspace / "result.json", record)
    try:
        runtime = backend.run_prompt(task_id=request["task_id"], query=request["query"], sandbox=workspace)
        record["runtime"] = runtime
        record["execution_status"] = "finished" if runtime["state"] == "succeeded" else "error"
        (workspace / "answer.md").write_text(runtime["final_message"], encoding="utf-8")
    except Exception as exc:
        record.update(execution_status="error", reason=f"{type(exc).__name__}: {exc}")
    record["wall_seconds"] = time.monotonic() - started
    write_json(workspace / "result.json", record)
    return record
