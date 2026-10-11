"""Native NU3 regressions; no model or quantum calculation is launched."""
from pathlib import Path

import pytest

from cloudra.tools.core.irc_evidence import verify_short_irc_direction

FIXTURES = Path(__file__).parent / "fixtures" / "benchmark_nu3"
pytest.importorskip('rdkit')


def test_irc_direction_requires_the_native_starting_ts():
    passed, details = verify_short_irc_direction(
        FIXTURES / "ts1_irc/irc.out",
        [FIXTURES / "ts2_frequency.out"],
        [FIXTURES / "mislabeled_rc_minimum.out"],
        [FIXTURES / "mislabeled_op_minimum.out"])
    assert not passed, details


