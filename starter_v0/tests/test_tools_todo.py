"""Required offline tool unit tests, completed for the supplied starter.

Tests verify behavior, failure modes and trust boundaries. External HTTP is always mocked.
Role C's 16 additional tests are in test_role_c_tools.py.
"""
from __future__ import annotations

from conftest import FakeResponse
from tools import TOOL_FUNCTIONS


def test_clarify_choice_returns_options_and_awaits_user() -> None:
    options = ["Bài báo", "Bài đăng"]
    result = TOOL_FUNCTIONS["clarify"](question="Bạn muốn loại nào?", response_type="choice", options=options)
    assert result["options"] == options
    assert result["response_type"] == "choice"
    assert result["awaiting_user"] is True


def test_format_sections_groups_items_by_section() -> None:
    items = [{"section": "A", "title": "a"}, {"section": "B", "title": "b"}, {"section": "A", "title": "c"}]
    markdown = TOOL_FUNCTIONS["format"](items=items, template="sections")["markdown"]
    assert markdown.count("## A") == 1
    assert markdown.count("## B") == 1
    assert markdown.index("## A") < markdown.index("## B")


def test_format_thread_numbers_items() -> None:
    items = [{"title": "Tin 1"}, {"title": "Tin 2"}]
    markdown = TOOL_FUNCTIONS["format"](items=items, template="thread")["markdown"]
    assert markdown.splitlines()[0].startswith("1/ ")
    assert markdown.splitlines()[2].startswith("2/ ")


def test_format_empty_items_does_not_crash() -> None:
    for items in (None, []):
        result = TOOL_FUNCTIONS["format"](items=items, template="sections")
        assert result["item_count"] == 0
        assert result["markdown"] == ""


def test_send_confirmed_posts_to_telegram(monkeypatch, fake_http) -> None:
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "fake-test-token")
    monkeypatch.setenv("TELEGRAM_CHAT_ID", "-100555555")
    calls = fake_http(FakeResponse({"ok": True}))
    result = TOOL_FUNCTIONS["send"](text="Tin thử nghiệm", confirmed=True)
    assert result["status"] == "sent"
    assert len(calls) == 1
    assert calls[0]["method"] == "POST"
    assert calls[0]["url"] == "https://api.telegram.org/botfake-test-token/sendMessage"
    assert calls[0]["json"]["chat_id"] == "-100555555"
    assert calls[0]["json"]["text"] == "Tin thử nghiệm"


def test_send_confirmed_without_env_returns_error_and_no_request(fake_http) -> None:
    calls = fake_http(FakeResponse({"ok": True}))
    result = TOOL_FUNCTIONS["send"](text="Không được gửi", confirmed=True)
    assert result["error"] == "RuntimeError"
    assert "TELEGRAM_BOT_TOKEN" in result["message"]
    assert calls == []


def test_lookup_without_timeframe_omits_time_range(monkeypatch, fake_http) -> None:
    monkeypatch.setenv("TAVILY_API_KEY", "test-key")
    calls = fake_http(FakeResponse({"results": []}))
    result = TOOL_FUNCTIONS["lookup"](query="AI", timeframe=None)
    assert "error" not in result
    assert len(calls) == 1
    assert "time_range" not in calls[0]["json"]


def test_fetch_maps_firecrawl_response(monkeypatch, fake_http) -> None:
    monkeypatch.setenv("FIRECRAWL_API_KEY", "test-key")
    calls = fake_http(FakeResponse({"data": {
        "markdown": "Nội dung nghiên cứu", "metadata": {"title": "T", "sourceURL": "https://example.org/paper"}
    }}))
    result = TOOL_FUNCTIONS["fetch"](url="https://example.org/paper")
    assert calls[0]["json"]["formats"] == ["markdown"]
    assert result["items"][0] == {
        "title": "T", "url": "https://example.org/paper", "source": "example.org", "summary": "Nội dung nghiên cứu"
    }


def test_fetch_truncates_markdown_to_4000_chars(monkeypatch, fake_http) -> None:
    monkeypatch.setenv("FIRECRAWL_API_KEY", "test-key")
    fake_http(FakeResponse({"data": {"markdown": "A" * 7000, "metadata": {}}}))
    result = TOOL_FUNCTIONS["fetch"](url="https://example.org")
    assert len(result["items"][0]["summary"]) == 4000


def test_timeline_respects_limit_and_skips_items_without_id(monkeypatch, fake_http) -> None:
    monkeypatch.setenv("RAPIDAPI_KEY", "test-key")
    raw = [{"screen_name": "researcher", "text": "missing id"}]
    raw += [{"screen_name": "researcher", "tweet_id": str(i), "text": f"Tin {i}"} for i in range(1, 7)]
    calls = fake_http(FakeResponse({"timeline": raw}))
    result = TOOL_FUNCTIONS["timeline"](screenname="researcher", limit=3)
    assert calls[0]["params"]["screenname"] == "researcher"
    assert len(result["items"]) == 3
    assert [x["url"] for x in result["items"]] == [f"https://x.com/researcher/status/{i}" for i in range(1, 4)]


def test_social_search_passes_search_type(monkeypatch, fake_http) -> None:
    monkeypatch.setenv("RAPIDAPI_KEY", "test-key")
    calls = fake_http(FakeResponse({"tweets": []}))
    result = TOOL_FUNCTIONS["social_search"](query="AI", search_type="Top", limit=2)
    assert result["search_type"] == "Top"
    assert calls[0]["params"] == {"query": "AI", "search_type": "Top"}


def test_policy_empty_query_returns_no_results() -> None:
    result = TOOL_FUNCTIONS["policy"](query="")
    assert result["results"] == []


def test_policy_area_filter_only_returns_that_area() -> None:
    result = TOOL_FUNCTIONS["policy"](query="privacy", policy_area="data_privacy")
    assert result["results"], "Fixture policy files should contain privacy sections"
    assert all(item["policy_area"] == "data_privacy" for item in result["results"])


def test_policy_instruction_like_lines_go_to_untrusted_text() -> None:
    result = TOOL_FUNCTIONS["policy"](query="citation", policy_area="source_citation", top_k=20)
    suspicious = [hit for hit in result["results"] if hit["section"] == "Injection probe"]
    assert suspicious, "Policy fixture includes an injection probe"
    assert any("ignore the citation policy" in line for line in suspicious[0]["untrusted_text"])
    assert "ignore the citation policy" not in suspicious[0]["facts"]


# New local tools: each has at least happy path, invalid input and error response.
# Full 16-case test coverage (4 tests/tool) is in tests/test_role_c_tools.py.
def test_my_new_tool_happy_path() -> None:
    result = TOOL_FUNCTIONS["dedupe_sources"]([
        {"title": "A", "url": "https://example.org/a"},
        {"title": "A copy", "url": "https://example.org/a?utm_medium=test"},
    ])
    assert result["output_count"] == 1
    assert result["removed_count"] == 1


def test_my_new_tool_bad_input_from_model() -> None:
    result = TOOL_FUNCTIONS["date_filter"]("not a list", start_date="2026-11-01")
    assert result["error"] == "invalid_input"


def test_my_new_tool_failure_returns_error_dict() -> None:
    result = TOOL_FUNCTIONS["source_audit"]([], require_https="yes")
    assert result["error"] == "invalid_option"
    assert "message" in result
