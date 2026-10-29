# The Quran data file

The kit does not ship Quran text. You supply your own file and point your workspace's `certainty.toml` at it
(`quran_data = "data/quran.json"`), or set `CERTAINTY_QURAN_DATA`. Use a text and a translation you have the
right to use, and record where they came from.

## Format

A JSON list with one record per verse:

```json
[
  {
    "verse_id": "1:1",
    "chapter_number": 1,
    "verse_number": 1,
    "verse_text_arabic": "بِسْمِ ٱللَّهِ ٱلرَّحْمَٰنِ ٱلرَّحِيمِ",
    "verse_text_arabic_clean": "بسم الله الرحمن الرحيم",
    "verse_text_english": "In the name of God, the Most Gracious, the Most Merciful.",
    "chapter_revelation_order": 5
  }
]
```

| Field | Required | What |
| --- | --- | --- |
| `verse_id` | yes | "chapter:verse" |
| `chapter_number`, `verse_number` | yes | integers; a verse that is not numbered (such as an unnumbered Basmalah) has verse_number 0 |
| `verse_text_arabic` | yes | the text with every mark, as it is written; the pen draws this |
| `verse_text_arabic_clean` | yes | the same text without vowel marks and without the small alef; the counts read this |
| `verse_text_english` | no | the translation, quoted verbatim on screen (footnote markers such as * are dropped) |
| `chapter_revelation_order` | no | for claims about the order of revelation |

`certainty data check` reports the file's shape and any problem: missing fields, repeated ids, vowel marks left
in the clean text.

## How letters and words are counted

- **Letters**: the Arabic letters and alef wasla of `verse_text_arabic_clean` (U+0621 to U+064A and U+0671). Vowel
  marks and the small alef are not letters. A hamza written above the line (U+0654) is not counted on its own.
- **Words**: split at spaces, as the text writes them.

Counting rules differ between editions and scholars. Say which rule a claim uses, in the script and on screen when
it matters, and never put a number on screen that a viewer with a printed copy of the same edition cannot recount.
