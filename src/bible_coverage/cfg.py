from typing import List
import pyparsing as pp

books = [
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
        "Obadiah",
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
        "Philemon",
        "Hebrews",
        "James",
        "Jude",
        "Revelation",
        "Obadiah",
        "Philemon",
        "Jude",
    ]
]

integer = pp.Word(pp.nums)


def isBibleBook(t) -> bool:
    return t[0] in books


parser = pp.Regex(r"\b[A-Za-z]+\b")
parser.addCondition(isBibleBook)


def parse(input: str) -> pp.ParseResults:
    return parser.parse_string(input)
