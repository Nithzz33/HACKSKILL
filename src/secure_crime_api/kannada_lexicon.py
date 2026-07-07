from __future__ import annotations

import re
from dataclasses import dataclass
from difflib import SequenceMatcher
from functools import lru_cache
from pathlib import Path
from typing import Any


KANNADA_WORD_RE = re.compile(r"[\u0c80-\u0cff]+")
RESOURCE_DIR = Path(__file__).with_name("resources") / "kannada"
DICTIONARY_PATH = RESOURCE_DIR / "kn_IN.dic"
AFFIX_PATH = RESOURCE_DIR / "kn_IN.aff"


@dataclass(frozen=True)
class KannadaLexicon:
    words: frozenset[str]
    entry_count: int
    replacements: tuple[tuple[str, str], ...]
    by_first_char: dict[str, tuple[str, ...]]


@lru_cache(maxsize=1)
def load_kannada_lexicon() -> KannadaLexicon:
    words, entry_count = _load_dictionary_words(DICTIONARY_PATH)
    replacements = _load_replacements(AFFIX_PATH)
    grouped: dict[str, list[str]] = {}
    for word in words:
        grouped.setdefault(word[:1], []).append(word)
    return KannadaLexicon(
        words=frozenset(words),
        entry_count=entry_count,
        replacements=tuple(replacements),
        by_first_char={key: tuple(sorted(values, key=len)) for key, values in grouped.items()},
    )


def dictionary_status() -> dict[str, Any]:
    lexicon = load_kannada_lexicon()
    return {
        "word_count": len(lexicon.words),
        "entry_count": lexicon.entry_count,
        "replacement_count": len(lexicon.replacements),
        "source_file": str(DICTIONARY_PATH),
        "affix_file": str(AFFIX_PATH),
    }


def normalize_kannada_query(query: str) -> dict[str, Any]:
    lexicon = load_kannada_lexicon()
    corrections: dict[str, str] = {}
    normalized = query
    for token in dict.fromkeys(KANNADA_WORD_RE.findall(query)):
        correction = best_kannada_match(token, lexicon)
        if correction and correction != token:
            corrections[token] = correction
            normalized = normalized.replace(token, correction)
    return {
        "normalized_query": normalized,
        "corrections": corrections,
        "dictionary": dictionary_status(),
    }


def best_kannada_match(token: str, lexicon: KannadaLexicon | None = None) -> str | None:
    word = token.strip()
    if len(word) < 3:
        return None
    lexicon = lexicon or load_kannada_lexicon()
    if word in lexicon.words:
        return word

    generated = _replacement_candidates(word, lexicon.replacements)
    for candidate in generated:
        if candidate in lexicon.words:
            return candidate

    pool = [
        candidate
        for candidate in lexicon.by_first_char.get(word[:1], ())
        if abs(len(candidate) - len(word)) <= 2
    ]
    best = None
    best_score = 0.0
    for candidate in pool[:2500]:
        score = SequenceMatcher(None, word, candidate).ratio()
        if score > best_score:
            best_score = score
            best = candidate
    return best if best and best_score >= 0.84 else None


def _replacement_candidates(word: str, replacements: tuple[tuple[str, str], ...]) -> set[str]:
    candidates = set()
    for source, target in replacements:
        if source == "0" or target == "0":
            continue
        if source in word:
            candidates.add(word.replace(source, target, 1))
    return candidates


def _load_dictionary_words(path: Path) -> tuple[set[str], int]:
    if not path.exists():
        return set(), 0
    words: set[str] = set()
    entry_count = 0
    for index, line in enumerate(path.read_text(encoding="utf-8").splitlines()):
        raw = line.strip()
        if not raw:
            continue
        if index == 0 and raw.isdigit():
            entry_count = int(raw)
            continue
        word = raw.split("/", 1)[0].strip()
        if KANNADA_WORD_RE.fullmatch(word) and len(word) >= 2:
            words.add(word)
    return words, entry_count or len(words)


def _load_replacements(path: Path) -> list[tuple[str, str]]:
    if not path.exists():
        return []
    replacements: list[tuple[str, str]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        raw = line.strip()
        if not raw.startswith("REP "):
            continue
        parts = raw.split()
        if len(parts) == 3:
            replacements.append((parts[1], parts[2]))
    return replacements
