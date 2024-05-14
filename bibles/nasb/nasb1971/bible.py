import os
import re
from typing import List
from model import Bible, Book, Chapter, Verse

def parse(bible_text_path: str = os.path.join(os.path.dirname(__file__), 'bible.txt')) -> Bible:
    books: Bible = []
    with open(bible_text_path) as file:
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

    return Bible('NASB 1971', books)
