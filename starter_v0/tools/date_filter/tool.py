"""Filter research items by published date without a network call."""
from datetime import date, datetime
from email.utils import parsedate_to_datetime


def _parse_date(value):
    if not isinstance(value, str) or not value.strip():
        return None
    value = value.strip()
    try:
        if len(value) == 10:
            return date.fromisoformat(value)
        return datetime.fromisoformat(value.replace("Z", "+00:00")).date()
    except (ValueError, TypeError):
        try:
            # Twitter/X often returns RFC 2822-like timestamps, e.g.
            # "Tue Nov 10 10:03:44 +0000 2026".
            return parsedate_to_datetime(value).date()
        except (ValueError, TypeError, IndexError):
            return None


def date_filter(items, start_date="", end_date="", include_undated=False):
    """Inclusive filtering on date/published metadata (ISO or RFC-like)."""
    if not isinstance(items, list) or any(not isinstance(x, dict) for x in items):
        return {"tool": "date_filter", "error": "invalid_input", "message": "items must be a list of objects"}
    if not isinstance(include_undated, bool):
        return {"tool": "date_filter", "error": "invalid_option", "message": "include_undated must be boolean"}
    if not isinstance(start_date, str) or not isinstance(end_date, str):
        return {"tool": "date_filter", "error": "invalid_date", "message": "bounds must be ISO date strings"}
    start = _parse_date(start_date) if start_date else None
    end = _parse_date(end_date) if end_date else None
    if not (start_date or end_date) or (start_date and start is None) or (end_date and end is None):
        return {"tool": "date_filter", "error": "invalid_date", "message": "provide at least one valid ISO date bound"}
    if start and end and start > end:
        return {"tool": "date_filter", "error": "invalid_range", "message": "start_date cannot exceed end_date"}
    result, undated = [], 0
    for item in items:
        raw = next((item[k] for k in ("published_at", "published_date", "published", "date", "created_at") if item.get(k)), None)
        published = _parse_date(raw)
        if published is None:
            undated += 1
            if include_undated:
                result.append(item)
        elif (start is None or published >= start) and (end is None or published <= end):
            result.append(item)
    return {"tool": "date_filter", "items": result, "input_count": len(items),
            "output_count": len(result), "undated_count": undated,
            "start_date": start_date, "end_date": end_date}
