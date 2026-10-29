"""The Quran data: load, check, and count from the file you supply (docs/data-format.md).

    certainty data check        report the file's shape and any problems

Letters are the written letters of verse_text_arabic_clean (Arabic letters and alef wasla; no marks, no small
alef). Words are split at spaces as the text writes them. Every number the kit puts on screen comes from here.
"""
import json
import re
from functools import lru_cache

from .settings import quran_data

REQUIRED = ("verse_id", "chapter_number", "verse_number", "verse_text_arabic", "verse_text_arabic_clean")
OPTIONAL = ("verse_text_english", "chapter_revelation_order")
LETTER = re.compile(r"[ء-يٱ]")


@lru_cache(maxsize=1)
def records():
    p = quran_data()
    if not p.exists():
        raise SystemExit(f"Quran data file not found: {p}")
    with open(p, encoding="utf-8") as fh:
        data = json.load(fh)
    if isinstance(data, dict):
        data = data.get("verses") or data.get("data") or list(data.values())
    return data


@lru_cache(maxsize=1)
def by_id():
    return {r["verse_id"]: r for r in records()}


def verse(vid):
    try:
        return by_id()[vid]
    except KeyError:
        raise SystemExit(f"verse {vid} is not in the data file")


def text(vid):
    return verse(vid)["verse_text_arabic_clean"]


def marked(vid):
    return verse(vid)["verse_text_arabic"]


def english(vid):
    """The verse's English, without footnote markers (a translation may mark footnotes with *)."""
    return re.sub(r"\s*\*+", "", verse(vid).get("verse_text_english", "")).strip()


def letters(s):
    return LETTER.findall(s)


def words(s):
    return s.split()


def verses(sura, unnumbered=False):
    """The verses of a sura in order; unnumbered ones (verse_number 0, such as an unnumbered Basmalah) only if asked."""
    out = [r for r in records() if r["chapter_number"] == sura and (unnumbered or r["verse_number"] > 0)]
    return sorted(out, key=lambda r: r["verse_number"])


def suras():
    return sorted({r["chapter_number"] for r in records()})


def check():
    """Problems with the file, and a short summary."""
    problems, recs = [], records()
    if not isinstance(recs, list) or not recs:
        return ["the file holds no list of verse records"], {}
    for k in REQUIRED:
        missing = sum(1 for r in recs if k not in r)
        if missing:
            problems.append(f"{missing} records have no '{k}'")
    if problems:
        return problems, {}
    ids = [r["verse_id"] for r in recs]
    if len(set(ids)) != len(ids):
        problems.append(f"{len(ids) - len(set(ids))} verse_id values repeat")
    bad = [r["verse_id"] for r in recs if r["verse_id"] != f"{r['chapter_number']}:{r['verse_number']}"
           and r["verse_number"] != 0]
    if bad:
        problems.append(f"{len(bad)} verse_id values do not read chapter:verse, e.g. {bad[:3]}")
    # vowel marks and the small alef must not be in the clean text (a hamza written above the line, U+0654, may be)
    with_marks = [r["verse_id"] for r in recs if re.search(r"[ً-ْٰ]", r["verse_text_arabic_clean"])]
    if with_marks:
        problems.append(f"verse_text_arabic_clean carries vowel marks in {len(with_marks)} records, "
                        f"e.g. {with_marks[:3]}")
    summary = dict(records=len(recs), suras=len(suras()), numbered=sum(1 for r in recs if r["verse_number"] > 0),
                   unnumbered=sum(1 for r in recs if r["verse_number"] == 0),
                   english=sum(1 for r in recs if r.get("verse_text_english")),
                   revelation_order=sum(1 for r in recs if r.get("chapter_revelation_order") is not None))
    return problems, summary


def main(argv):
    if not argv or argv[0] != "check":
        raise SystemExit("usage: certainty data check")
    print(f"Quran data: {quran_data()}")
    problems, summary = check()
    for k, v in summary.items():
        print(f"  {k:17} {v}")
    for p in problems:
        print(f"  PROBLEM  {p}")
    if "1:1" in by_id():
        print(f"  1:1 letters      {len(letters(text('1:1')))}")
    return 1 if problems else 0
