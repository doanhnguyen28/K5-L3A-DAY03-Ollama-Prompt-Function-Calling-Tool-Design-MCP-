"""Audit the structural quality of source records, not the truthfulness of content."""
from urllib.parse import urlsplit
from tools.dedupe_sources.tool import canonical_url


def source_audit(items, require_https=False):
    """Report missing fields, invalid URLs, duplicate URLs, and HTTP links."""
    if not isinstance(items, list) or any(not isinstance(x, dict) for x in items):
        return {"tool": "source_audit", "error": "invalid_input", "message": "items must be a list of objects"}
    if not isinstance(require_https, bool):
        return {"tool": "source_audit", "error": "invalid_option", "message": "require_https must be boolean"}
    issues, seen, valid = [], set(), 0
    for index, item in enumerate(items):
        local = []
        title = item.get("title")
        if not isinstance(title, str) or not title.strip():
            local.append("missing_title")
        url = item.get("url")
        canon = canonical_url(url)
        if not canon:
            local.append("invalid_or_missing_url")
        else:
            if canon in seen:
                local.append("duplicate_url")
            seen.add(canon)
            if require_https and urlsplit(url.strip()).scheme.lower() != "https":
                local.append("non_https_url")
        summary = item.get("summary")
        if not isinstance(summary, str) or not summary.strip():
            local.append("missing_summary")
        if local:
            issues.append({"index": index, "codes": local})
        else:
            valid += 1
    return {"tool": "source_audit", "total_count": len(items),
            "structurally_complete_count": valid, "issues": issues,
            "note": "Structural checks only; this does not verify factual accuracy, author credibility, or website safety."}
