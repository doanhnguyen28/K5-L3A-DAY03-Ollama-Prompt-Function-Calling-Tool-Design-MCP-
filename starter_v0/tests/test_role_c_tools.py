"""Offline regression tests for four new Role C tools."""
from tools.dedupe_sources.tool import dedupe_sources
from tools.date_filter.tool import date_filter
from tools.source_audit.tool import source_audit
from tools.keyword_extract.tool import keyword_extract

# dedupe_sources: standard, normalized URL, title fallback, guards

def test_dedupe_removes_utm_and_fragment():
    data = [{"title": "a", "url": "https://www.example.org/news/?utm_source=x#one"},
            {"title": "b", "url": "http://example.org/news"},
            {"title": "c", "url": "https://other.org/"}]
    result = dedupe_sources(data)
    assert result["removed_count"] == 1 and [x["title"] for x in result["items"]] == ["a", "c"]


def test_dedupe_falls_back_to_title():
    result = dedupe_sources([{"title": "AI Research"}, {"title": " ai   research "}])
    assert result["output_count"] == 1


def test_dedupe_keep_last():
    result = dedupe_sources([{"title": "A", "summary": "old"}, {"title": "a", "summary": "new"}], "last")
    assert result["items"][0]["summary"] == "new"


def test_dedupe_bad_input_returns_error_dict():
    assert dedupe_sources("wrong")["error"] == "invalid_input"
    assert dedupe_sources([], keep="unknown")["error"] == "invalid_keep"

# date_filter: inclusive date boundaries, ISO timestamps, missing metadata, bad args

def test_date_filter_inclusive_bounds():
    data = [{"date": "2026-11-01"}, {"published_at": "2026-11-10T10:20:00+07:00"}, {"date": "2026-11-11"}]
    result = date_filter(data, "2026-11-01", "2026-11-10")
    assert result["output_count"] == 2


def test_date_filter_undated_option():
    data = [{"title": "unknown"}, {"date": "2026-11-02"}]
    assert date_filter(data, start_date="2026-11-01")["output_count"] == 1
    assert date_filter(data, start_date="2026-11-01", include_undated=True)["output_count"] == 2


def test_date_filter_reversed_range_returns_error():
    assert date_filter([], "2026-12-01", "2026-11-01")["error"] == "invalid_range"


def test_date_filter_invalid_input_returns_error():
    assert date_filter("x", start_date="2026-11-01")["error"] == "invalid_input"
    assert date_filter([], "bad")["error"] == "invalid_date"
    assert date_filter([])["error"] == "invalid_date"

# source_audit: valid fields, missing data, duplicated URLs, guards

def test_source_audit_complete_source():
    result = source_audit([{"title": "Paper", "url": "https://arxiv.org/abs/1", "summary": "Content"}])
    assert result["structurally_complete_count"] == 1 and result["issues"] == []


def test_source_audit_reports_missing_fields():
    result = source_audit([{"title": ""}])
    assert set(result["issues"][0]["codes"]) == {"missing_title", "invalid_or_missing_url", "missing_summary"}


def test_source_audit_reports_duplicates_and_http():
    data = [{"title": "A", "url": "http://example.com/x", "summary": "x"},
            {"title": "B", "url": "https://example.com/x?utm_source=test", "summary": "y"}]
    result = source_audit(data, require_https=True)
    assert "non_https_url" in result["issues"][0]["codes"]
    assert "duplicate_url" in result["issues"][1]["codes"]


def test_source_audit_bad_input_returns_error():
    assert source_audit({"url": "abc"})["error"] == "invalid_input"
    assert source_audit([], require_https="yes")["error"] == "invalid_option"

# keyword_extract: frequency, language, empty, invalid bounds

def test_keywords_rank_frequency():
    result = keyword_extract("Python agent. Python research. Agent AI.", 2)
    assert result["keywords"][0] == {"keyword": "python", "count": 2}
    assert result["keywords"][1] == {"keyword": "agent", "count": 2}


def test_keywords_keep_vietnamese_words():
    result = keyword_extract("Nghiên cứu mô hình. Nghiên cứu trí tuệ nhân tạo.", 8)
    assert {x["keyword"] for x in result["keywords"]} >= {"nghiên", "cứu", "mô", "hình"}


def test_keywords_empty_returns_error_dict():
    assert keyword_extract("   ")["error"] == "invalid_text"
    assert keyword_extract(None)["error"] == "invalid_text"


def test_keywords_invalid_max_returns_error_dict():
    assert keyword_extract("AI", 0)["error"] == "invalid_limit"
    assert keyword_extract("AI", True)["error"] == "invalid_limit"
    assert keyword_extract("AI", 25)["error"] == "invalid_limit"


def test_date_filter_accepts_arxiv_and_social_date_formats():
    data = [
        {"title": "arXiv paper", "published": "2026-11-09T12:15:00Z"},
        {"title": "social post", "date": "Tue Nov 10 10:03:44 +0000 2026"},
        {"title": "older", "created_at": "Mon, 02 Nov 2026 13:00:00 GMT"},
    ]
    result = date_filter(data, start_date="2026-11-09", end_date="2026-11-10")
    assert [x["title"] for x in result["items"]] == ["arXiv paper", "social post"]
