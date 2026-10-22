"""Preserve standard-arm scope: standalone verification off, geometry still available."""
from unittest.mock import Mock

import pytest

from cloudra.tools.Chemtool.ts_guess import TsGuess, TsGuess_input_schema, TsGuess_output_schema


@pytest.mark.parametrize("strict", [False, True])
@pytest.mark.asyncio
async def test_standalone_verification_is_disabled_without_reading_logs(mock_session, strict, monkeypatch):
    tool = TsGuess()
    verifier = Mock(side_effect=AssertionError("native verifier must not run"))
    monkeypatch.setattr(tool, "_verify", verifier)
    result = await tool.tool_call(TsGuess_input_schema(mode="verify", freq_log="absent.log", strict=strict), mock_session)
    assert not result.is_success
    assert "Verification is disabled" in result.message
    verifier.assert_not_called()


@pytest.mark.parametrize("mode", ["interpolate", "xtb_path", "scan_parse"])
@pytest.mark.asyncio
async def test_non_verification_helpers_remain_dispatchable(mock_session, monkeypatch, mode):
    tool = TsGuess()
    handler = Mock(return_value=TsGuess_output_schema(is_success=True, message="local helper probe"))
    monkeypatch.setattr(tool, "_" + mode, handler)
    arguments = ({"log_path": "scan.log"} if mode == "scan_parse" else
                 {"reactant_text": "1\nreactant\nH 0 0 0\n", "product_text": "1\nproduct\nH 0 0 1\n"})
    result = await tool.tool_call(TsGuess_input_schema(mode=mode, **arguments), mock_session)
    assert result.is_success and result.message == "local helper probe"
    handler.assert_called_once()
