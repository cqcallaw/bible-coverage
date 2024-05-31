import pyparsing
import pytest

import bible_coverage.parser.parser as parser
import bible_coverage.bibles.nasb.nasb1971.bible as bible

# forms:
# <book><chapter>
# <book><verse range>
# <book><chapter>:<verse range>
# <book><chapter>:<verse range>[<optional verse range>]
# <book><chapter>:<verse range>;<verse range>[<optional verse range>]
# <book><chapter>:[<optional verse range>]<verse range>
# <section> or <section>


nasb_bible = bible.parse()


def test_verse_parse() -> None:
    result = parser.startVerse.parse_string("2")
    assert len(result) == 1
    assert result.start_verse == 2


def test_verse_range_parse() -> None:
    result = parser.verseRange.parse_string("2-9")
    assert len(result) == 1
    assert result.verse_range.start == 2
    assert result.verse_range.end == 9


def test_verse_range_parse_single() -> None:
    result = parser.verseRange.parse_string("3")
    assert len(result) == 1
    assert result.verse_range.start == 3
    assert result.verse_range.end == 3


def test_verse_range_list() -> None:
    result = parser.verseRangeList.parse_string("1-3, 7, 8-10")
    assert len(result) == 3
    assert result[0].start == 1
    assert result[0].end == 3
    assert result[1].start == 7
    assert result[1].end == 7
    assert result[2].start == 8
    assert result[2].end == 10


def test_chapter() -> None:
    result = parser.chapterRangeList.parse_string("3")
    assert result.chapter_range_list[0].start == 3
    assert result.chapter_range_list[0].end == 3


def test_book() -> None:
    result = parser.book.parse_string("Genesis")
    assert result.book == "Genesis"


def test_chapter_and_verse_range() -> None:
    result = parser.chapterAndVerseRanges.parse_string("3:1-10")
    assert result.chapter_and_verse_ranges.chapter == 3
    assert len(result.chapter_and_verse_ranges.verseRanges) == 1
    assert result.chapter_and_verse_ranges.verseRanges[0].start == 1
    assert result.chapter_and_verse_ranges.verseRanges[0].end == 10


def test_chapter_and_verse_ranges() -> None:
    result = parser.chapterAndVerseRanges.parse_string("3:1-10, 12-15")
    assert result.chapter_and_verse_ranges.chapter == 3
    assert len(result.chapter_and_verse_ranges.verseRanges) == 2
    assert result.chapter_and_verse_ranges.verseRanges[0].start == 1
    assert result.chapter_and_verse_ranges.verseRanges[0].end == 10
    assert result.chapter_and_verse_ranges.verseRanges[1].start == 12
    assert result.chapter_and_verse_ranges.verseRanges[1].end == 15


def test_reference() -> None:
    result = parser.reference.parse_string("Genesis 3:1-10")
    assert result.reference.book == "Genesis"
    assert isinstance(
        result.reference.chapterRangesAndVerseRanges,
        parser.model.ChapterAndVerseRanges,
    )
    assert result.reference.chapterRangesAndVerseRanges.chapter == 3
    assert len(result.reference.chapterRangesAndVerseRanges.verseRanges) == 1

    assert result.reference.chapterRangesAndVerseRanges.verseRanges[0].start == 1
    assert result.reference.chapterRangesAndVerseRanges.verseRanges[0].end == 10


def test_genesis() -> None:
    result = parser.getNormalizedReferences("Genesis 1:1", nasb_bible)
    assert len(result) == 1
    assert result[0].book == "Genesis"
    assert result[0].chapter == 1
    assert result[0].verse == 1


def test_whole_psalm() -> None:
    result = parser.getNormalizedReferences("Psalm 100", nasb_bible)
    assert len(result) == 4
    assert result[0].book == "Psalms"
    assert result[0].chapter == 100
    assert result[0].verse == 1
    assert result[1].verse == 2
    assert result[2].verse == 3
    assert result[3].verse == 4


def test_whole_short_book() -> None:
    result = parser.getNormalizedReferences("Jude", nasb_bible)
    assert len(result) == 25
    assert result[0].book == "Jude"
    assert result[0].chapter == 1
    assert result[0].verse == 1


def test_short_book_verse() -> None:
    result = parser.getNormalizedReferences("Jude 3", nasb_bible)
    assert len(result) == 1
    assert result[0].book == "Jude"
    assert result[0].chapter == 1
    assert result[0].verse == 3


def test_invalid() -> None:
    with pytest.raises(pyparsing.exceptions.ParseException):
        _ = parser.getNormalizedReferences("Enoch 1:1", nasb_bible)


def test_basic_range() -> None:
    result = parser.getNormalizedReferences("Genesis 15:1-6", nasb_bible)
    assert len(result) == 6
    assert result[0].book == "Genesis"
    assert result[0].chapter == 15
    assert result[0].verse == 1


def test_optional_range() -> None:
    result = parser.getNormalizedReferences("Luke 2:1-14 [15-20]", nasb_bible)
    assert len(result) == 20
    assert result[0].book == "Luke"
    assert result[0].chapter == 2
    assert result[0].verse == 1
    assert result[19].chapter == 2
    assert result[19].verse == 20


def test_second_disjunct_ranges() -> None:
    result = parser.getNormalizedReferences("Isaiah 1:1, 10-20", nasb_bible)
    assert len(result) == 2
    assert result[0].book == "Isaiah"
    assert result[0].chapter == 2
    assert result[0].start_verse == 1
    assert result[0].end_verse == 1
    assert result[1].book == "Isaiah"
    assert result[1].chapter == 2
    assert result[1].start_verse == 10
    assert result[1].start_verse == 20


def test_disjunct_books() -> None:
    result = parser.getNormalizedReferences(
        "Galatians 4:4-7 or Philippians 2:5-11", nasb_bible
    )
    assert len(result) == 2


def test_verse_a_start() -> None:
    result = parser.getNormalizedReferences("Amos 6:1a, 4-7", nasb_bible)
    assert len(result) == 5
    assert result[0].book == "Amos"
    assert result[0].chapter == 6
    assert result[0].verse == 1
    assert result[1].book == "Amos"
    assert result[1].chapter == 6
    assert result[1].verse == 4
    assert result[4].book == "Amos"
    assert result[4].chapter == 6
    assert result[4].verse == 7


def test_verse_a_end() -> None:
    result = parser.getNormalizedReferences("Revelation 21:1-6a", nasb_bible)
    assert len(result) == 6
    assert result[0].book == "Revelation"
    assert result[0].chapter == 21
    assert result[0].verse == 1
    assert result[5].book == "Revelation"
    assert result[5].chapter == 21
    assert result[5].verse == 6


def test_verse_b_start() -> None:
    result = parser.getNormalizedReferences("Romans 10:8b-13", nasb_bible)
    assert len(result) == 6
    assert result[0].book == "Romans"
    assert result[0].chapter == 10
    assert result[0].verse == 8
    assert result[5].book == "Romans"
    assert result[5].chapter == 10
    assert result[5].verse == 13


def test_verse_b_end() -> None:
    result = parser.getNormalizedReferences("Romans 12:9-16b", nasb_bible)
    assert len(result) == 8
    assert result[0].book == "Romans"
    assert result[0].chapter == 12
    assert result[0].verse == 9
    assert result[7].book == "Romans"
    assert result[7].chapter == 12
    assert result[7].verse == 16


def test_multiple_ranges() -> None:
    result = parser.getNormalizedReferences("Nehemiah 8:1-3, 5-6, 8-10", nasb_bible)
    assert len(result) == 8


def test_multiple_ranges_multiple_styles() -> None:
    result = parser.getNormalizedReferences("Nehemiah 8:1-3, 7, 8-10", nasb_bible)
    assert len(result) == 7


def test_multiple_chapter_ranges() -> None:
    result = parser.getNormalizedReferences(
        "Ecclesiastes 1:2, 12-14; 2:18-23", nasb_bible
    )
    assert len(result) == 3


def test_extra_verse_ranges() -> None:
    result = parser.getNormalizedReferences("Ecclesiastes 1:100", nasb_bible)
    assert len(result) == 0


if __name__ == "__main__":
    pytest.main()
