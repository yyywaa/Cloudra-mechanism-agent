"""Role permission / tool-policy stage.

The stage consults PipelineContext.capabilities plus registry projections
(visual gate, role allowlist); it has no knowledge of specific tools.  New
tool classes become visible automatically when the runtime capability filter
builds the tools list.
"""

from __future__ import annotations

from cloudra.runtime_v2.policies.base import PipelineContext, PolicyResult, ToolCall
from cloudra.tools.capabilities import missing_permissions, role_hidden_tools, visual_tools


class PermissionStage:
    name = "permission"

    async def before_tool(self, ctx: PipelineContext, call: ToolCall) -> PolicyResult:
        tools = set(ctx.capabilities.tools)
        if "*" not in tools and call.name not in tools:
            return PolicyResult.block(
                f"tool {call.name!r} is not in this agent's capabilities "
                f"(available: {sorted(tools)})"
            )
        if not ctx.settings.visual_mode and call.name in visual_tools():
            return PolicyResult.block(
                f"tool {call.name!r} requires visual mode, which is off for this agent; "
                "turn it on with /visual to use vision tools"
            )
        if call.name in role_hidden_tools(ctx.agent.role_id):
            return PolicyResult.block(
                f"tool {call.name!r} is restricted to specific roles and is not "
                f"available to role {ctx.agent.role_id!r}"
            )
        # 统一权限闸（评审 5.6）：角色 PermissionSet 必须覆盖工具在
        # ToolRegistration.required_permissions 里声明的每一位；工具类内部的
        # is_* 检查是第二道闸。未注册/注入式工具无声明，按原样放行。
        missing = missing_permissions(ctx.capabilities.permissions, call.name)
        if missing:
            return PolicyResult.block(
                f"tool {call.name!r} requires role permission(s) {sorted(missing)}, "
                f"which role {ctx.agent.role_id!r} does not grant "
                "(declared in ToolRegistration.required_permissions)"
            )
        return PolicyResult.allow()

    async def after_tool(self, ctx: PipelineContext, call: ToolCall, result) -> None:
        return None

    async def before_llm(self, ctx: PipelineContext, messages: list[dict]) -> None:
        return None
