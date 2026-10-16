"""Run original Aitomia questions on Cloudra; retain evidence for independent review."""

from __future__ import annotations

import argparse
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

from cloudra.benchmark.aitomia import execute_case, load_catalog, prepare_case, write_json


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--list", action="store_true", help="list the 47 original cases; no model calls")
    parser.add_argument("--only", default="", help="comma-separated original task IDs")
    parser.add_argument("--data-dir", type=Path, default=Path("aitomia_benchmark_data"))
    parser.add_argument("--input", action="append", default=[], metavar="TASK_ID=FILE.xyz",
                        help="bind an original geometry input; repeatable")
    parser.add_argument("--run", action="store_true", help="execute Cloudra (default: prepare inputs only)")
    args = parser.parse_args(argv)
    catalog = load_catalog()
    known = {case.task_id for case in catalog.cases}
    wanted = {value.strip() for value in args.only.split(",") if value.strip()}
    if wanted - known:
        print(f"unknown task IDs: {sorted(wanted - known)}", file=sys.stderr)
        return 2
    cases = [case for case in catalog.cases if not wanted or case.task_id in wanted]
    inputs = {}
    for binding in args.input:
        task_id, sep, filename = binding.partition("=")
        path = Path(filename).expanduser().resolve()
        if not sep or task_id not in {case.task_id for case in cases} or not path.is_file():
            parser.error(f"invalid --input: {binding}; expected a selected TASK_ID and an existing file")
        inputs[task_id] = path
    if args.list:
        for case in cases:
            requirement = "requires original XYZ" if case.provided_xyz else "no supplied XYZ required"
            print(f"{case.task_id}\t{case.level}\t{requirement}")
        return 0

    run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "-" + uuid4().hex[:8]
    run_dir = args.data_dir.expanduser().resolve() / run_id
    run_dir.mkdir(parents=True)
    records = [prepare_case(case, run_dir / f"case-{case.source_row - 2:02d}", inputs.get(case.task_id))
               for case in cases]
    manifest = {
        "run_id": run_id,
        "source": catalog.source,
        "cases": [case.model_dump(mode="json") for case in cases],
        "mode": "run" if args.run else "prepare",
        "scoring": "unreviewed; no public per-case references or automatic scorer",
        "results": records,
    }
    write_json(run_dir / "run.json", manifest)
    print(f"run directory: {run_dir}", flush=True)
    if args.run:
        # Same isolation as the native benchmark CLI; never save these settings
        # to the user's configuration or attach to an existing live project.
        isolated = run_dir / "runtime"
        os.environ["CLOUDRA_DATA_DIR"] = str(isolated)
        from cloudra.infra.config import get_config

        get_config().data_dir = isolated
        from cloudra.benchmark.backend import RuntimeV2Backend
        from cloudra.benchmark.runner import provenance_config

        manifest["configuration"] = provenance_config("runtime_v2", [])
        write_json(run_dir / "run.json", manifest)
        backend = RuntimeV2Backend(store_path=isolated / "runtime-v2.db")
        for index, record in enumerate(records):
            print(f"{record['task_id']}: {record['execution_status']}", flush=True)
            records[index] = execute_case(record, backend)
            manifest["results"] = records
            write_json(run_dir / "run.json", manifest)
    for record in records:
        print(f"{record['task_id']}: {record['execution_status']}; scientific review pending", flush=True)
    return int(args.run and any(record["execution_status"] != "finished" for record in records))


if __name__ == "__main__":
    sys.exit(main())
