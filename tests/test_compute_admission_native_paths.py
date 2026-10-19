"""Native Link0 file references must stay inside the task workspace.

The failure these cover: a hand-written input declared
``%chk=/.../sandboxes/jobs/ep4/end_b_optfreq.chk`` (missing the task/batch
level), so a Gaussian job created a checkpoint outside its own sandbox. The
check is ownership-only: paths are never rewritten and files are never
required to exist, so same-task cross-job restarts keep working.
"""

from __future__ import annotations

from pathlib import Path

from cloudra.services.compute_admission import (
    admit_job,
    native_file_references,
    native_path_violation,
)


def _workspace(tmp_path: Path) -> Path:
    root = tmp_path / 'sandboxes' / 'D1' / 'batch_x'
    (root / 'jobs' / 'ep4').mkdir(parents=True)
    (root / 'jobs' / 'ep5').mkdir(parents=True)
    return root


def test_references_parse_quoted_values():
    assert native_file_references('%chk="a b.chk"\n%oldchk=old.chk\n') == [
        ('%chk', 'a b.chk'), ('%oldchk', 'old.chk'),
    ]


def test_in_workspace_and_same_task_cross_job_reuse_are_allowed(tmp_path):
    root = _workspace(tmp_path)
    content = f'%oldchk={root}/jobs/ep4/a.chk\n%chk={root}/jobs/ep5/b.chk\n#p opt=Restart\n'
    assert native_path_violation(content, workdir=str(root / 'jobs' / 'ep5'), workspace_root=str(root)) is None


def test_new_output_checkpoint_need_not_exist(tmp_path):
    root = _workspace(tmp_path)
    content = f'%chk={root}/jobs/ep5/brand-new.chk\n#p opt\n'
    assert native_path_violation(content, workdir=str(root / 'jobs' / 'ep5'), workspace_root=str(root)) is None


def test_reference_outside_the_task_workspace_is_reported(tmp_path):
    root = _workspace(tmp_path)
    outside = tmp_path / 'sandboxes' / 'jobs'
    outside.mkdir(parents=True)
    content = f'%chk={outside}/a.chk\n#p opt=Restart\n'
    message = native_path_violation(content, workdir=str(root / 'jobs' / 'ep5'), workspace_root=str(root))
    assert message is not None
    assert str(outside / 'a.chk') in message
    assert 'never rewritten' in message


def test_relative_reference_resolves_against_the_execution_directory(tmp_path):
    root = _workspace(tmp_path)
    content = '%chk=local.chk\n#p opt\n'
    assert native_path_violation(content, workdir=str(root / 'jobs' / 'ep5'), workspace_root=str(root)) is None


def test_admit_job_rejects_out_of_workspace_reference(tmp_path):
    root = _workspace(tmp_path)
    outside = tmp_path / 'outside'
    outside.mkdir()
    input_path = root / 'jobs' / 'ep5' / 'run.gjf'
    input_path.write_text(
        f'%chk={outside}/a.chk\n%nproc=1\n%mem=1GB\n#p opt b3lyp/def2svp\n\ntitle\n\n0 1\nH 0 0 0\n',
        encoding='utf-8',
    )
    outcome = admit_job(
        input_file=str(input_path), job_type='gaussian', cpus=1, memory_mb=1024,
        workspace_root=str(root),
    )
    assert outcome.ok is False
    assert 'outside this task workspace' in outcome.message


def test_admit_job_keeps_ordinary_semantics_without_workspace_root(tmp_path):
    """No workspace_root: admission must not gain a new absolute-path restriction."""
    root = _workspace(tmp_path)
    outside = tmp_path / 'outside'
    outside.mkdir()
    input_path = root / 'jobs' / 'ep5' / 'run.gjf'
    input_path.write_text(
        f'%chk={outside}/a.chk\n%nproc=1\n%mem=1GB\n#p opt b3lyp/def2svp\n\ntitle\n\n0 1\nH 0 0 0\n',
        encoding='utf-8',
    )
    outcome = admit_job(input_file=str(input_path), job_type='gaussian', cpus=1, memory_mb=1024)
    assert 'outside this task workspace' not in outcome.message
