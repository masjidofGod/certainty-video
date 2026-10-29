"""Count from the data, and check an episode's claims before any of them goes on screen.

    certainty count letters 1:1            19
    certainty count words 96:1-5           how many words in 96:1 to 96:5
    certainty count verses 96              verses in sura 96
    certainty count letter ب 1             how many times a letter is written in sura 1
    certainty verify <episode>/claims.toml  every claim against the data; exit 1 if any differs

A claim is a statement, what kind of count proves it, and the number it states. Only claims that match may be
drawn or spoken; the episode's timeline reads the counts from here, never from typed numbers.

    [[claim]]
    id = "basmalah-letters"
    says = "The Basmalah (1:1) has 19 letters"
    kind = "letters"          # letters | words | verses | letter | suras | unnumbered
    verses = "1:1"            # one verse, a range "96:1-5", or a list ["1:1", "27:30"]
    stated = 19
"""
import tomllib

from . import data


def expand(spec):
    """'1:1', '96:1-5' or a list of those -> verse ids."""
    if isinstance(spec, list):
        return [v for s in spec for v in expand(s)]
    sura, rest = spec.split(":")
    if "-" in rest:
        a, b = rest.split("-")
        return [f"{sura}:{n}" for n in range(int(a), int(b) + 1)]
    return [spec]


def count(kind, **a):
    if kind == "letters":
        return sum(len(data.letters(data.text(v))) for v in expand(a["verses"]))
    if kind == "words":
        return sum(len(data.words(data.text(v))) for v in expand(a["verses"]))
    if kind == "verses":
        return len(data.verses(int(a["sura"])))
    if kind == "letter":
        suras = a["sura"] if isinstance(a["sura"], list) else [a["sura"]]
        return sum(data.letters(r["verse_text_arabic_clean"]).count(a["letter"])
                   for s in suras for r in data.verses(int(s)))
    if kind == "suras":
        return len(data.suras())
    if kind == "unnumbered":
        return sum(1 for r in data.records() if r["verse_number"] == 0)
    raise SystemExit(f"unknown kind of count: {kind}")


def load(path):
    with open(path, "rb") as fh:
        return tomllib.load(fh).get("claim", [])


def check(path):
    rows = []
    for c in load(path):
        args = {k: v for k, v in c.items() if k not in ("id", "says", "kind", "stated")}
        got = count(c["kind"], **args)
        rows.append(dict(id=c["id"], says=c.get("says", ""), stated=c["stated"], measured=got,
                         ok=got == c["stated"]))
    return rows


def measured(path, cid):
    """A claim's number, for a timeline to draw: only if it matches what the claim states."""
    for r in check(path):
        if r["id"] == cid:
            assert r["ok"], f"claim {cid} differs: stated {r['stated']}, the data gives {r['measured']}"
            return r["measured"]
    raise KeyError(cid)


def main(argv, verify=False):
    if verify:
        if not argv:
            raise SystemExit("usage: certainty verify <claims.toml>")
        rows = check(argv[0])
        print("| id | claim | stated | measured | |\n| --- | --- | --- | --- | --- |")
        for r in rows:
            print(f"| {r['id']} | {r['says']} | {r['stated']} | {r['measured']} | {'match' if r['ok'] else 'DIFFERS'} |")
        bad = [r for r in rows if not r["ok"]]
        print(f"{len(rows)} claims, {len(bad)} differ")
        return 1 if bad else 0
    if not argv:
        raise SystemExit(__doc__)
    kind, rest = argv[0], argv[1:]
    if kind in ("letters", "words"):
        print(count(kind, verses=rest[0]))
    elif kind == "verses":
        print(count(kind, sura=rest[0]))
    elif kind == "letter":
        print(count(kind, letter=rest[0], sura=rest[1]))
    else:
        print(count(kind))
    return 0
