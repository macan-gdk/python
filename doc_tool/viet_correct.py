"""Hậu xử lý OCR tiếng Việt: khôi phục dấu theo từ điển + bigram."""

from __future__ import annotations

import json
import re
import unicodedata
from functools import lru_cache

from doc_tool.bootstrap import DATA_DIR

_WORD_RE = re.compile(r"[A-Za-zÀ-ỹà-ỹĐđ]+", flags=re.UNICODE)
_TOKEN_RE = re.compile(
    r"[a-zàáảãạăằắẳẵặâầấẩẫậèéẻẽẹêềếểễệìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵđ]+",
    flags=re.I,
)


def to_base(s: str) -> str:
    """Bỏ dấu tiếng Việt (dat ≈ đất)."""
    s = s.lower().replace("đ", "d").replace("Đ", "d")
    nk = unicodedata.normalize("NFD", s)
    return "".join(c for c in nk if unicodedata.category(c) != "Mn")


def has_diacritics(s: str) -> bool:
    return s.lower() != to_base(s)


def edit_distance(a: str, b: str) -> int:
    if a == b:
        return 0
    if not a:
        return len(b)
    if not b:
        return len(a)
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(
                min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb))
            )
        prev = cur
    return prev[-1]


def restore_case(original: str, suggestion: str) -> str:
    if original.isupper():
        return suggestion.upper()
    if original[:1].isupper():
        return suggestion[:1].upper() + suggestion[1:]
    return suggestion


@lru_cache(maxsize=1)
def load_lexicon() -> dict:
    """base_index / words / bigrams / unigram từ data/."""
    base_path = DATA_DIR / "vi_base_index.json"
    words_path = DATA_DIR / "vi_words.txt"

    base_index: dict[str, list[str]] = {}
    if base_path.is_file():
        base_index = json.loads(base_path.read_text(encoding="utf-8"))

    words: set[str] = set()
    bigrams: dict[tuple[str, str], int] = {}
    unigram: dict[str, int] = {}

    if words_path.is_file():
        for line in words_path.read_text(encoding="utf-8").splitlines():
            raw = line.strip().lower()
            if not raw:
                continue
            parts = _TOKEN_RE.findall(raw)
            for p in parts:
                words.add(p)
                unigram[p] = unigram.get(p, 0) + 1
            for i in range(len(parts) - 1):
                key = (parts[i], parts[i + 1])
                bigrams[key] = bigrams.get(key, 0) + 1

    return {
        "base_index": base_index,
        "words": words,
        "bigrams": bigrams,
        "unigram": unigram,
    }


def _bigram_hits(
    cand: str, prev: str | None, nxt: str | None, lex: dict
) -> int:
    bigrams: dict = lex["bigrams"]
    hits = 0
    if prev:
        hits += bigrams.get((prev.lower(), cand), 0)
    if nxt:
        hits += bigrams.get((cand, nxt.lower()), 0)
        if not has_diacritics(nxt):
            for nc in lex["base_index"].get(to_base(nxt.lower()), []):
                if has_diacritics(nc):
                    hits += bigrams.get((cand, nc), 0)
    return hits


def _rank(
    cand: str,
    ocr_token: str,
    prev: str | None,
    nxt: str | None,
    lex: dict,
) -> tuple:
    return (
        -_bigram_hits(cand, prev, nxt, lex),
        -lex["unigram"].get(cand, 0),
        edit_distance(ocr_token.lower(), cand),
        0 if has_diacritics(cand) else 1,
    )


def _pick_best(
    candidates: list[str],
    lower: str,
    prev: str | None,
    nxt: str | None,
    lex: dict,
) -> str | None:
    if not candidates:
        return None
    return min(candidates, key=lambda c: _rank(c, lower, prev, nxt, lex))


def _should_skip(token: str) -> bool:
    return len(token) <= 1 or bool(re.search(r"\d", token))


def correct_token(
    token: str, prev: str | None, nxt: str | None, lex: dict
) -> str:
    if _should_skip(token):
        return token

    lower = token.lower()
    words: set[str] = lex["words"]
    base_index: dict = lex["base_index"]
    candidates = list(base_index.get(to_base(lower), []))
    if not candidates:
        return token

    # Đã có dấu + trong từ điển → giữ
    if lower in words and has_diacritics(lower):
        return token

    # Không dấu → chỉ thêm dấu khi bigram thắng rõ
    if not has_diacritics(lower):
        accented = [c for c in candidates if has_diacritics(c)]
        best = _pick_best(accented, lower, prev, nxt, lex)
        if best is None:
            return token
        best_bg = _bigram_hits(best, prev, nxt, lex)
        bare_bg = _bigram_hits(lower, prev, nxt, lex) if lower in words else 0
        if best_bg <= 0 or best_bg <= bare_bg:
            return token
        return restore_case(token, best)

    # OOV có dấu lệch
    if lower not in words:
        best = _pick_best(candidates, lower, prev, nxt, lex)
        if best is None or edit_distance(lower, best) > 2:
            return token
        return restore_case(token, best)

    return token


def fix_vietnamese_ocr(text: str) -> str:
    """Khôi phục dấu cho toàn bộ chuỗi OCR."""
    lex = load_lexicon()
    tokens = list(_WORD_RE.finditer(text))
    if not tokens:
        return text

    words = [m.group(0) for m in tokens]
    corrected: list[str] = []
    for i, w in enumerate(words):
        prev = corrected[i - 1] if i else None
        nxt = words[i + 1] if i + 1 < len(words) else None
        corrected.append(correct_token(w, prev, nxt, lex))

    parts: list[str] = []
    last = 0
    for match, new_w in zip(tokens, corrected):
        parts.append(text[last : match.start()])
        parts.append(new_w)
        last = match.end()
    parts.append(text[last:])
    fixed = "".join(parts)

    lines = []
    for line in fixed.splitlines():
        s = line.strip()
        if len(s) <= 2 and not re.search(r"[A-Za-zÀ-ỹ0-9]", s):
            continue
        lines.append(line)
    return "\n".join(lines)
