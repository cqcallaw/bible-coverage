import re
from typing import List

class Verse():
    def __init__(self, number: int, text):
        self.__number = number
        self.__text = text

    @property
    def number(self) -> int:
        return self.__number

    @property
    def text(self) -> str:
        return self.__text

class Chapter():
    def __init__(self, number: int, verses: List[Verse]):
        self.__number = number
        self.__verses = verses

    @property
    def number(self) -> int:
        return self.__number

    @property
    def verses(self) -> List[Verse]:
        return self.__verses

class Book():
    def __init__(self, name: str, chapters: List[Chapter]):
        self.__name = name
        self.__chapters = chapters

    @property
    def name(self) -> str:
        return self.__name

    @property
    def chapters(self) -> List[Chapter]:
        return self.__chapters

class Bible():
    def __init__(self, books: List[Book]):
        self.__books = books

    @property
    def books(self) -> List[Book]:
        return self.__books

class NasbBible(Bible):
    def parse(text: str) -> Bible:
        books: Bible = []
        with open(text) as file:
            current_book_name: str = 'Genesis'
            current_book_list: List[Book] = []
            current_chapter_list: List[Chapter] = []
            current_chapter_number: int = 1
            current_chapter_verses: List[Verse] = []

            while line := file.readline():
                line = line.strip()

                verse_match = re.match("(\d+) (.*)", line)
                if verse_match:
                    verse = Verse(int(verse_match.group(1)), verse_match.group(2))
                    current_chapter_verses.append(verse)

                chapter_header_match = re.match("([a-zA-Z]+)\s*(\d+)", line)
                if chapter_header_match:
                    matched_book_name = chapter_header_match.group(1)
                    matched_chapter_number = int(chapter_header_match.group(2))

                    if current_chapter_number != matched_chapter_number:
                        # chapter boundary
                        current_chapter_list.append(Chapter(current_chapter_number, current_chapter_verses))
                        current_chapter_verses = []
                        current_chapter_number = matched_chapter_number
                    if current_book_name != matched_book_name:
                        # book boundary
                        books.append(Book(current_book_name, current_chapter_list))
                        current_book_name = matched_book_name
                        current_chapter_list = []

        # handle final chapter
        current_book_list.append(Chapter(current_chapter_number, current_chapter_verses))
        books.append(Book(current_book_name, current_chapter_list))

        return NasbBible(books)

# NASB Bible from https://archive.org/download/nasb-new-american-standard-bible-nasb/NASB%20New%20American%20Standard%20Bible%20%28NASB%29_hocr.html
bible = NasbBible.parse('nasb.txt')

for book in bible.books:
    for chapter in book.chapters:
        for verse in chapter.verses:
            print (f"{book.name} {chapter.number}:{verse.number}")

