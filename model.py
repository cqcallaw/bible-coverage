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
    def __init__(self, name: str, books: List[Book]):
        self.__name = name
        self.__books = books

    @property
    def name(self) -> str:
        return self.__name

    @property
    def books(self) -> List[Book]:
        return self.__books
