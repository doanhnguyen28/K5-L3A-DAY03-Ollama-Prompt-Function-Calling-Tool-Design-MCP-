"""Simple transparent frequency-based keyword extraction; no AI or network."""
import re
from collections import Counter

_STOPWORDS = {
    "và", "của", "cho", "trong", "một", "những", "các", "với", "là", "được", "trên", "này",
    "về", "theo", "khi", "để", "từ", "mới", "có", "không", "đang", "đã", "cần", "the", "and",
    "for", "with", "that", "this", "from", "are", "was", "were", "have", "has", "into",
    "you", "your", "their", "about", "what", "where", "when", "how", "can", "will", "its",
    "an", "is", "of", "to", "be", "in", "on", "at", "as", "or", "by", "do", "it", "no", "if", "we", "he", "so", "us"
}


def keyword_extract(text, max_keywords=8):
    """Return top repeated words, with counts and deterministic tie-breaking."""
    if not isinstance(text, str) or not text.strip():
        return {"tool": "keyword_extract", "error": "invalid_text", "message": "text must be nonempty"}
    if isinstance(max_keywords, bool) or not isinstance(max_keywords, int) or not 1 <= max_keywords <= 20:
        return {"tool": "keyword_extract", "error": "invalid_limit", "message": "max_keywords must be an integer from 1 to 20"}
    tokens = re.findall(r"[^\W\d_]+", text, flags=re.UNICODE)
    words = [w.lower() for w in tokens if len(w) >= 2 and w.lower() not in _STOPWORDS]
    counts = Counter(words)
    first = {word: words.index(word) for word in counts}
    ordered = sorted(counts, key=lambda word: (-counts[word], first[word]))[:max_keywords]
    return {"tool": "keyword_extract", "keywords": [{"keyword": w, "count": counts[w]} for w in ordered],
            "total_tokens": len(tokens), "candidate_tokens": len(words),
            "method": "word_frequency_no_semantic_understanding"}
