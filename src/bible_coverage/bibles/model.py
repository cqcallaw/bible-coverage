from collections import OrderedDict


Chapter = OrderedDict[int, str]
Book = OrderedDict[int, Chapter]
NamedBookList = OrderedDict[str, Book]


class Bible:
    def __init__(self, name: str, books: NamedBookList):
        self.__name = name
        self.__books = books

    @property
    def name(self) -> str:
        return self.__name

    @property
    def books(self) -> NamedBookList:
        return self.__books


class Plan:
    def __init__(self, name: str, books: NamedBookList):
        self.__name = name
        self.__books = books

    @property
    def name(self) -> str:
        return self.__name

    @property
    def books(self) -> NamedBookList:
        return self.__books
