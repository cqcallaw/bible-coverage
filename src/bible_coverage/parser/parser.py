from . import model
import logging
from typing import List
import pyparsing as pp
import pythonbible as pb

logger = logging.getLogger(__name__)

integer = pp.Word(pp.nums).set_parse_action(lambda toks: int(toks[0]))


bookList = [
    pb.Book.GENESIS,
    pb.Book.EXODUS,
    pb.Book.LEVITICUS,
    pb.Book.NUMBERS,
    pb.Book.DEUTERONOMY,
    pb.Book.JOSHUA,
    pb.Book.JUDGES,
    pb.Book.RUTH,
    pb.Book.SAMUEL_1,
    pb.Book.SAMUEL_2,
    pb.Book.KINGS_1,
    pb.Book.KINGS_2,
    pb.Book.CHRONICLES_1,
    pb.Book.CHRONICLES_2,
    pb.Book.EZRA,
    pb.Book.NEHEMIAH,
    pb.Book.ESTHER,
    pb.Book.JOB,
    pb.Book.PSALMS,
    pb.Book.PROVERBS,
    pb.Book.ECCLESIASTES,
    pb.Book.SONG_OF_SONGS,
    pb.Book.ISAIAH,
    pb.Book.JEREMIAH,
    pb.Book.LAMENTATIONS,
    pb.Book.EZEKIEL,
    pb.Book.DANIEL,
    pb.Book.HOSEA,
    pb.Book.JOEL,
    pb.Book.AMOS,
    pb.Book.JONAH,
    pb.Book.MICAH,
    pb.Book.NAHUM,
    pb.Book.HABAKKUK,
    pb.Book.ZEPHANIAH,
    pb.Book.HAGGAI,
    pb.Book.ZECHARIAH,
    pb.Book.MALACHI,
    pb.Book.MATTHEW,
    pb.Book.MARK,
    pb.Book.LUKE,
    pb.Book.JOHN,
    pb.Book.ACTS,
    pb.Book.ROMANS,
    pb.Book.CORINTHIANS_1,
    pb.Book.CORINTHIANS_2,
    pb.Book.GALATIANS,
    pb.Book.EPHESIANS,
    pb.Book.PHILIPPIANS,
    pb.Book.COLOSSIANS,
    pb.Book.THESSALONIANS_1,
    pb.Book.THESSALONIANS_2,
    pb.Book.TIMOTHY_1,
    pb.Book.TIMOTHY_2,
    pb.Book.TITUS,
    pb.Book.HEBREWS,
    pb.Book.JAMES,
    pb.Book.PETER_1,
    pb.Book.PETER_2,
    pb.Book.JOHN_1,
    pb.Book.REVELATION,
    pb.Book.ESDRAS_1,
    pb.Book.TOBIT,
    pb.Book.WISDOM_OF_SOLOMON,
    pb.Book.ECCLESIASTICUS,
    pb.Book.MACCABEES_1,
    pb.Book.MACCABEES_2,
    pb.Book.OBADIAH,
    pb.Book.PHILEMON,
    pb.Book.JUDE,
    pb.Book.JOHN_2,
    pb.Book.JOHN_3,
]

book_title_normalizers = [(book, book.title) for book in bookList]


def generate_book_title_parse_action(title):
    # can't use lambda in list comprehension because of how the closure works
    return lambda: title


book = pp.Or(
    [
        # match regex and map it to the normalized book title
        pp.Regex(book.regular_expression).set_parse_action(
            generate_book_title_parse_action(book.title)
        )
        for book in bookList
    ]
).set_results_name("book")

startVerse = (
    (integer + "a" | integer + "b" | integer)
    # integer
    .set_results_name("start_verse")
    .set_parse_action(lambda toks: toks[0])
)
endVerse = startVerse.set_results_name("end_verse")

verseRange = (
    ((startVerse + "-" + endVerse) | startVerse)
    .set_results_name("verse_range")
    .set_parse_action(model.VerseRange)
)
verseRangeList = (
    pp.DelimitedList(verseRange, delim=",")
    .set_results_name("verse_range_list")
    .set_parse_action(model.VerseRangeList)
)

startChapter = integer.set_results_name("start_chapter")
endChapter = integer.set_results_name("end_chapter")
chapterRange = (
    ((startChapter + "-" + endChapter) | startChapter)
    .set_results_name("chapter_range")
    .set_parse_action(model.ChapterRange)
)
chapterRangeList = (
    pp.DelimitedList(chapterRange, delim=",")
    .set_results_name("chapter_range_list")
    .set_parse_action(model.ReferenceRangeSpecifier)
)

chapterAndVerseRanges = (
    (startChapter + ":" + pp.Group(verseRangeList))
    .set_results_name("chapter_and_verse_ranges")
    .set_parse_action(model.ChapterAndVerseRanges)
)
chapterAndVerseRangesList = (
    pp.DelimitedList(expr=chapterAndVerseRanges, delim=";")
    .set_results_name("chapter_and_verse_range_list")
    .set_parse_action(model.ReferenceRangeSpecifier)
)

multiChapterRange = (
    (startChapter + ":" + startVerse + "-" + endChapter + ":" + endVerse)
    .set_results_name("multi_chapter_range")
    .set_parse_action(model.MultiChapterRange)
)
multiChapterRangeList = (
    pp.DelimitedList(multiChapterRange)
    .set_results_name("multi_chapter_range_list")
    .set_parse_action(model.ReferenceRangeSpecifier)
)

verseRangeSpecifiers = (
    multiChapterRangeList | chapterAndVerseRangesList | chapterRangeList
).set_results_name("range_specifiers")

reference = (
    (book + pp.Opt(verseRangeSpecifiers))
    .set_results_name("reference")
    .set_parse_action(model.Reference)
)


def getNormalizedReferences(input: str, bible) -> List[model.NormalizedReference]:
    parseResult = reference.parseString(input, parse_all=False)
    refs = parseResult.reference.chapterRangesAndVerseRanges.getNormalizedReferences(
        bible, parseResult.reference.book
    )
    return list(refs)
