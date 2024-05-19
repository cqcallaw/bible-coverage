from functools import reduce
import logging
from typing import Optional
import pyparsing as pp
import pythonbible as pb

logger = logging.getLogger(__name__)


chapteredBook = pp.Or(
    [
        pp.Regex(book.regular_expression).setResultsName(book.title)
        for book in [
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
            pb.Book.JOHN_2,
            pb.Book.JOHN_3,
            pb.Book.REVELATION,
            pb.Book.ESDRAS_1,
            pb.Book.TOBIT,
            pb.Book.WISDOM_OF_SOLOMON,
            pb.Book.ECCLESIASTICUS,
            pb.Book.MACCABEES_1,
            pb.Book.MACCABEES_2,
        ]
    ]
).setResultsName("book")


singleChapterBook = pp.Or(
    [
        pp.Regex(book.regular_expression).setResultsName(book.title)
        for book in [
            pb.Book.OBADIAH,
            pb.Book.PHILEMON,
            pb.Book.JUDE,
        ]
    ]
).setResultsName("book")

integer = pp.Word(pp.nums).setParseAction(lambda toks: int(toks[0]))


startVerse = integer.setResultsName("start_verse")
endVerse = integer.setResultsName("end_verse")
verseRange = (startVerse + "-" + endVerse).setResultsName("verse_range")
verseOrVerseRange = verseRange | startVerse
chapter = integer.setResultsName("chapter")
chapterAndVerseParser = chapter + pp.Opt(":" + verseOrVerseRange)
mainParser = (chapteredBook + pp.Opt(chapterAndVerseParser)) | (
    singleChapterBook + pp.Opt(verseOrVerseRange)
)


def parse(input: str) -> Optional[pp.ParseResults]:
    result = mainParser.parseString(input, parse_all=False)
    return result
