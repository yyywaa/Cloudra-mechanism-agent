from typing import Any

from pydantic import Field

from cloudra.base.session_class import Session
from cloudra.base.tool_actor import ToolActorContext
from cloudra.base.tools_class import Tool, input_schema, output_schema
from cloudra.runtime_v2.roles import dispatch_roster

description = (
    "Launch a sub-agent to run a specific task. The Coordinator may split a complex job into subtasks.\n"
    "Important guidelines:\n"
    "- **Absolute paths**: you must provide the working directory's absolute path in query or context.\n"
    "- **Safety**: permissions and operation approvals are enforced by runtime policy. Explain intent, target paths and rollback for risky operations.\n"
    "- **Task definition**: the task description must be extremely specific: name the tools to use, and explicitly forbid tools unrelated to the task.\n"
    "- **AgentHub**: sub-agents can share findings/questions/answers with other parallel Agents via `agent_hub`, and can address someone with to_agent (posts are public; addressees and authors of replied-to posts are notified). When dispatching overlapping work, tell them to check the hub first and post conclusions to the hub.\n"
    "- **agent_id**: pass a role id such as explorer, writer, researcher, small_mol, md, dft, experiment, env. The same role can be dispatched repeatedly; historical a-N aliases remain accepted.\n"
    "Available sub-agents (generated from the role profiles):\n"
    + dispatch_roster()
)


class SubAgentLauncher_input_schema(input_schema):
    agent_id: str = Field(description="Role id of the sub-agent (explorer, writer, researcher, small_mol, md, dft, experiment, env); historical a-N aliases remain accepted.")
    query: str = Field(
        description=(
            "Task description. Write only what this task needs, not the sub-agent's identity (already injected via prompt). "
            "Must include: goal, required absolute paths/input data, allowed tools, forbidden tools, output format, and done criteria."
        )
    )
    context: list = Field(
        default_factory=list,
        description=(
            "Initial context messages for the sub-agent. "
            "Each element must be a standard message dict {\"role\": \"user\"/\"system\"/\"assistant\", \"content\": \"...\"}; "
            "do not pass plain strings."
        )
    )
    is_wait: bool = Field(
        default=False,
        description="Whether to wait until the sub-agent finishes. True blocks until the task completes and returns the result; False fires the task and returns immediately."
    )


class SubAgentLauncher_output_schema(output_schema):
    is_success: bool = Field(default=False, description="Whether the dispatch succeeded")
    session_id: str = Field(description="Sub-agent Session ID")
    act_agent: str = Field(description="Name of the Agent that actually ran the task")
    result: str = Field(description="Sub-agent's final result")


class SubAgentLauncher(Tool):
    tool_id: str = 't-0'
    tool_name: str = 'subagent_launcher'
    tool_description: str = description
    input_schema: Any = SubAgentLauncher_input_schema
    output_schema: Any = SubAgentLauncher_output_schema
    subagent: ToolActorContext | None = None

    def is_manage(self) -> bool:
        return True

    async def tool_call(
        self,
        input_instance: SubAgentLauncher_input_schema,
        session: Session
    ) -> SubAgentLauncher_output_schema:
        # Legacy 派发已删除；runtime_v2 的 LegacyToolExecutor 在执行前按工具名
        # 拦截到 subagent_bridge，此 body 只是兜底。
        return SubAgentLauncher_output_schema(
            is_success=False,
            session_id="error",
            act_agent="none",
            result="[System error] SubAgentLauncher is handled by runtime_v2; the legacy dispatch path no longer exists.",
        )

    def get_subagents(self) -> list[str]:
        return []


def get_class():
    return SubAgentLauncher
