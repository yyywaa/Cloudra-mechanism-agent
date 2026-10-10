"""Document preloading is a durable first-task phase, not a new agent."""
import pytest

from cloudra.runtime_v2.schemas import Command
from cloudra.runtime_v2.turn_pipeline import LLMResponse
from tests.agent_scenarios import ScenarioHarness, ScriptedProvider, Step


class ChooseRead(ScriptedProvider):
    async def select_tool_names(self, agent, messages, *, resolved_settings):
        await super().select_tool_names(agent,messages,resolved_settings=resolved_settings)
        return LLMResponse(content='["read"]',usage={'input_tokens':7})


@pytest.mark.asyncio
async def test_tool_documents_preload_once_and_survive_new_task(tmp_path, monkeypatch):
    provider=ChooseRead(default=[Step(stop=True)])
    harness=await ScenarioHarness.start(tmp_path,provider=provider)
    try:
        agent=await harness.spawn('coordinator',query='Inspect actual evidence input')
        await harness.wait_terminal(agent)
        assert len(getattr(provider,'selection_calls',[]))==1
        assert 'Inspect actual evidence input' in str(provider.selection_calls[0][1])
        context=harness.core.session_contexts[agent.id]
        record=context.prefix_meta['tool_selection']
        assert record['status']=='selected'
        assert record['names']==['read']
        documents=[m for m in context.messages if m.get('tool_documents')]
        assert [item['name'] for item in documents[0]['tool_documents']]==['read']
        original_caps=list(agent.capabilities.tools)
        original_revision=record['document_revisions']['read']
        from cloudra.tools import get_tools_lst
        read_entry=next(entry for entry in get_tools_lst() if entry.tool_name=='read')
        monkeypatch.setattr(read_entry,'tool_description',read_entry.tool_description+' New contract revision.')
        provider.script_default(Step(stop=True))
        await harness.bus.execute(Command(type='agent.message',target={'session_id':agent.id},payload={'content':'Another task'}))
        await harness.wait_for(lambda:provider.call_count()==2,'second main request')
        await harness.wait_terminal(agent)
        assert len(provider.selection_calls)==1
        assert agent.capabilities.tools==original_caps
        changed=harness.core.session_contexts[agent.id].prefix_meta['tool_selection']
        assert changed['document_revisions']['read'] != original_revision
    finally:
        await harness.aclose()


@pytest.mark.asyncio
async def test_tool_selection_failure_still_allows_main_task(tmp_path):
    class Broken(ScriptedProvider):
        async def select_tool_names(self,*args,**kwargs):
            raise RuntimeError('No selection service')
    provider=Broken(default=[Step(stop=True)])
    harness=await ScenarioHarness.start(tmp_path,provider=provider)
    try:
        agent=await harness.spawn('coordinator',query='Read evidence')
        await harness.wait_terminal(agent)
        assert provider.call_count()==1
        record=harness.core.session_contexts[agent.id].prefix_meta['tool_selection']
        assert record['status']=='failed'
        assert record['error_code']=='RuntimeError'
    finally:
        await harness.aclose()


@pytest.mark.asyncio
async def test_empty_agent_defers_selection_and_interrupted_selection_restores_without_retry(tmp_path):
    from cloudra.runtime_v2.tool_selection import ToolSelectionRecord
    provider=ChooseRead(default=[Step(stop=True)])
    harness=await ScenarioHarness.start(tmp_path,provider=provider)
    agent=await harness.spawn('coordinator',query='')
    await harness.settle()
    assert getattr(provider,'selection_calls',[])==[]
    record=ToolSelectionRecord(status='started',source='llm',catalog_revision='revision',selection_id='attempt')
    await harness.core.contexts.record_tool_selection(agent=agent,run_id='interrupted',record=record,messages=[])
    await harness.aclose()
    resumed_provider=ChooseRead(default=[Step(stop=True)])
    restored=await ScenarioHarness.restore(tmp_path,provider=resumed_provider)
    try:
        resumed=restored.core.agents[agent.id]
        await restored.bus.execute(Command(type='agent.message',target={'session_id':resumed.id},payload={'content':'Read evidence now'}))
        await restored.wait_terminal(resumed)
        assert getattr(resumed_provider,'selection_calls',[])==[]
        state=restored.core.session_contexts[agent.id].prefix_meta['tool_selection']
        assert state['status']=='failed'
        assert state['error_code']=='selection_interrupted'
    finally:
        await restored.aclose()


@pytest.mark.asyncio
async def test_compacted_selection_restores_but_explicit_restart_selects_again(tmp_path):
    provider = ChooseRead(default=[Step(stop=True)])
    harness = await ScenarioHarness.start(tmp_path, provider=provider)
    agent = await harness.spawn('coordinator', query='Read first task')
    await harness.wait_terminal(agent)
    state = harness.core.contexts.prefix_state(agent.id)
    assert await harness.core.contexts.install_compacted(
        agent=agent, run_id='compact', messages=[{'role': 'assistant', 'content': 'Summary'}],
        prefix_meta=state['meta'], expected_version=len(state['messages']), trigger='test',
    )
    await harness.aclose()
    resumed_provider = ChooseRead(default=[Step(stop=True)])
    restored = await ScenarioHarness.restore(tmp_path, provider=resumed_provider)
    try:
        resumed = restored.core.agents[agent.id]
        await restored.bus.execute(Command(type='agent.message', target={'session_id': resumed.id},
            payload={'content': 'Continue after compact'}))
        await restored.wait_for(lambda: resumed_provider.call_count() == 1, 'resumed main request')
        await restored.wait_terminal(resumed)
        assert getattr(resumed_provider, 'selection_calls', []) == []
        assert restored.core.session_contexts[resumed.id].prefix_meta['tool_selection']['names'] == ['read']
        resumed_provider.script_default(Step(stop=True))
        await restored.bus.execute(Command(type='agent.restart', target={'session_id': resumed.id},
            payload={'message': 'Fresh context task'}))
        await restored.wait_for(lambda: resumed_provider.call_count() == 2, 'reset main request')
        await restored.wait_terminal(resumed)
        assert len(resumed_provider.selection_calls) == 1
    finally:
        await restored.aclose()
