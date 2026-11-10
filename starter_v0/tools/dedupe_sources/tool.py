"""Deduplicate research source dictionaries without network access."""
from urllib.parse import urlsplit, urlunsplit, parse_qsl, urlencode

_TRACKING = {"fbclid", "gclid", "msclkid", "igshid", "ref_src", "ref_url"}


def canonical_url(url):
    """Return a canonical HTTP URL, or empty string for invalid URLs."""
    if not isinstance(url, str) or not url.strip():
        return ""
    try:
        parts = urlsplit(url.strip())
        if parts.scheme.lower() not in ("http", "https") or not parts.hostname:
            return ""
        host = parts.hostname.lower()
        if host.startswith("www."):
            host = host[4:]
        port = parts.port
        if port and not (parts.scheme.lower() == "http" and port == 80) and not (parts.scheme.lower() == "https" and port == 443):
            host += ":" + str(port)
        path = parts.path.rstrip("/") or "/"
        query = urlencode(sorted((k, v) for k, v in parse_qsl(parts.query, keep_blank_values=True)
                               if not k.lower().startswith("utm_") and k.lower() not in _TRACKING))
        return urlunsplit(("https", host, path, query, ""))
    except (ValueError, TypeError):
        return ""


def dedupe_sources(items, keep="first"):
    """Remove duplicates by normalized URL, else normalized title."""
    if not isinstance(items, list) or any(not isinstance(x, dict) for x in items):
        return {"tool": "dedupe_sources", "error": "invalid_input", "message": "items must be a list of objects"}
    if keep not in ("first", "last"):
        return {"tool": "dedupe_sources", "error": "invalid_keep", "message": "keep must be 'first' or 'last'"}
    chosen = {}
    order = range(len(items)) if keep == "first" else range(len(items) - 1, -1, -1)
    for ix in order:
        item = items[ix]
        url = canonical_url(item.get("url"))
        title = item.get("title", "")
        title = " ".join(title.lower().split()) if isinstance(title, str) else ""
        key = ("url", url) if url else (("title", title) if title else ("unique", ix))
        if key not in chosen:
            chosen[key] = ix
    kept_indexes = sorted(chosen.values())
    unique_items = [items[i] for i in kept_indexes]
    return {"tool": "dedupe_sources", "items": unique_items,
            "input_count": len(items), "output_count": len(unique_items),
            "removed_count": len(items) - len(unique_items)}
