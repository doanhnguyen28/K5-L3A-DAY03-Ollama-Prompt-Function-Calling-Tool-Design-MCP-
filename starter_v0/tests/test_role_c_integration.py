"""Proves a new tool is declared, callable by the agent, and executed offline."""
from pathlib import Path

from agent import ResearchAgent
from providers.base import ModelResponse, ToolCall
from tools import TOOL_FUNCTIONS, load_tool_declarations, to_openai_tools


class OfflineFakeProvider:
    """Known pre-programmed response; no model or network request."""
    def complete(self, messages, tools=None, *, model=None, temperature=0.0, tool_choice=None):
        return ModelResponse(text=None, tool_calls=[ToolCall(
            name="source_audit", args={"items": [{"title": "A", "url": "", "summary": "news"}]}
        )])


def test_agent_executes_new_declared_tool_offline():
    root = Path(__file__).resolve().parents[1]
    declarations = load_tool_declarations(root / "artifacts" / "tools.yaml")
    assert "source_audit" in {item["name"] for item in declarations}
    assert "source_audit" in TOOL_FUNCTIONS
    agent = ResearchAgent(OfflineFakeProvider(), system_prompt="offline test", tools=to_openai_tools(declarations))
    result = agent.run([{"role": "user", "content": "Kiểm tra nguồn này"}])
    assert result.tool_results[0]["tool"] == "source_audit"
    assert result.tool_results[0]["result"]["issues"][0]["codes"] == ["invalid_or_missing_url"]
