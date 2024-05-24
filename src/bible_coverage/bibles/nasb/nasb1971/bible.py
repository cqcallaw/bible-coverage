import os
import re
from bible_coverage.bibles.model import Bible, Book, Chapter, NamedBookList


def parse(
    bible_text_path: str = os.path.join(os.path.dirname(__file__), "bible.txt"),
) -> Bible:
    books = NamedBookList()
    with open(bible_text_path) as file:
        current_book_name: str = "Genesis"
        current_chapter_number: int = 1
        current_book = Book()
        current_chapter = Chapter()

        while line := file.readline():
            line = line.strip()

            verse_match = re.match("(\d+) (.*)", line)
            if verse_match:
                verse_number = int(verse_match.group(1))
                verse_text = verse_match.group(2)
                current_chapter[verse_number] = verse_text

            chapter_header_match = re.match("([a-zA-Z]+)\s*(\d+)", line)
            if chapter_header_match:
                matched_book_name = chapter_header_match.group(1)
                matched_chapter_number = int(chapter_header_match.group(2))

                if current_chapter_number != matched_chapter_number:
                    # chapter boundary
                    current_book[current_chapter_number] = current_chapter
                    current_chapter = Chapter()
                    current_chapter_number = matched_chapter_number
                if current_book_name != matched_book_name:
                    # book boundary
                    books[current_book_name] = current_book
                    current_book = Book()
                    current_chapter_number = 1
                    current_book_name = matched_book_name

    # handle final chapter
    current_book[current_chapter_number] = current_chapter
    books[current_book_name] = current_book

    return Bible("NASB 1971", books)
