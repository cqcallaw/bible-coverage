import logging
from typing import Optional
import pyparsing as pp

logger = logging.getLogger(__name__)


chapteredBooks = [
    pp.Keyword(book)
    for book in [
        "Genesis",
        "Exodus",
        "Leviticus",
        "Numbers",
        "Deuteronomy",
        "Joshua",
        "Judges",
        "Ruth",
        "Ezra",
        "Nehemiah",
        "Esther",
        "Job",
        "Psalms",
        "Psalm",
        "Proverbs",
        "Ecclesiastes",
        "Isaiah",
        "Jeremiah",
        "Lamentations",
        "Ezekiel",
        "Daniel",
        "Hosea",
        "Joel",
        "Amos",
        "Jonah",
        "Micah",
        "Nahum",
        "Habakkuk",
        "Zephaniah",
        "Haggai",
        "Zechariah",
        "Malachi",
        "Matthew",
        "Mark",
        "Luke",
        "John",
        "Acts",
        "Romans",
        "Galatians",
        "Ephesians",
        "Philippians",
        "Colossians",
        "Titus",
        "Hebrews",
        "James",
        "Revelation",
        "Sirach",
    ]
]

singleChapterBooks = [
    pp.Keyword(book)
    for book in [
        "Obadiah",
        "Philemon",
        "Jude",
    ]
]

integer = pp.Word(pp.nums)


def isChapterBibleBook(t) -> bool:
    return t[0] in chapteredBooks


def isSingleChaperBibleBook(t) -> bool:
    return t[0] in singleChapterBooks


chapteredBookParser = (
    pp.Regex(r"\b[A-Za-z]+\b").addCondition(isChapterBibleBook).setResultsName("book")
)
singleChapterBookParser = (
    pp.Regex(r"\b[A-Za-z]+\b")
    .addCondition(isSingleChaperBibleBook)
    .setResultsName("book")
)

verseParser = pp.Opt(integer).setResultsName("verse")
chapterParser = pp.Opt(integer).setResultsName("chapter")
chapterAndVerseParser = pp.Opt(chapterParser + pp.Opt(":" + verseParser))
mainParser = (chapteredBookParser + chapterAndVerseParser) | (
    singleChapterBookParser + verseParser
)


def parse(input: str) -> Optional[pp.ParseResults]:
    result = mainParser.parseString(input, parse_all=False)
    return result
