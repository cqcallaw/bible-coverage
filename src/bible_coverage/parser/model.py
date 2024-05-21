from abc import abstractmethod
from typing import Iterable, List, Union


class Verse:
    __number: int

    def __init__(self, tokens):
        self.__number = int(tokens[0])

    @property
    def number(self) -> int:
        return self.__number


class Chapter:
    __number: int

    def __init__(self, tokens):
        self.__number = int(tokens[0])

    @property
    def number(self) -> int:
        return self.__number


class VerseRange:
    __start: Verse
    __end: Verse

    def __init__(self, tokens):
        if len(tokens) == 1:
            # single verse
            self.__start = tokens[0]
            self.__end = tokens[0]
        else:
            self.__start = tokens[0]
            self.__end = tokens[2]

    @property
    def start(self) -> Verse:
        return self.__start

    @property
    def end(self) -> Verse:
        return self.__end

    def getAllVerses(self) -> Iterable[Verse]:
        return (
            verse
            for verse in range(
                self.start.number,
                self.end.number + 1,  # inclusive range end
            )
        )


class VerseRangeList(list):
    def __init__(self, tokens):
        super().__init__(tokens)

    def getAllVerses(self) -> Iterable[Verse]:
        return (verse for verseRange in self for verse in verseRange.getAllVerses())


class ChapterRange:
    __start: Chapter
    __end: Chapter

    def __init__(self, tokens):
        if len(tokens) == 1:
            # single Chapter
            self.__start = tokens[0]
            self.__end = tokens[0]
        else:
            self.__start = tokens[0]
            self.__end = tokens[2]

    @property
    def start(self) -> Chapter:
        return self.__start

    @property
    def end(self) -> Chapter:
        return self.__end

class NormalizedReference:
    __book: str
    __chapter: int
    __verse: int

    def __init__(self, book: str, chapter: int, verse: int):
        self.__book = book
        self.__chapter = chapter
        self.__verse = verse

    @property
    def book(self) -> str:
        return self.__book

    @property
    def chapter(self) -> int:
        return self.__chapter

    @property
    def verse(self) -> int:
        return self.__verse


class ChapterAndVerseRanges:
    __chapter: Chapter
    __verseRanges: VerseRangeList

    def __init__(self, tokens):
        self.__chapter = tokens[0]
        self.__verseRanges = tokens[2]

    @property
    def chapter(self) -> Chapter:
        return self.__chapter

    @property
    def verseRanges(self) -> VerseRangeList:
        return self.__verseRanges

    def getNormalizedReferences(
        self, bible, book: str
    ) -> Iterable[NormalizedReference]:
        return (
            NormalizedReference(book, self.chapter, verse.number)
            for verseRange in self.verseRanges
            for verse in verseRange.getAllVerses()
        )


class MultiChapterRange:
    __startChapter: Chapter
    __startVerse: Verse
    __endChapter: Chapter
    __endVerse = Verse

    def __init__(self, tokens):
        self.__startChapter = tokens[0]
        self.__startVerse = tokens[1]
        self.__endChapter = tokens[2]
        self.__endVerse = tokens[3]

    @property
    def startChapter(self) -> Chapter:
        return self.__startChapter

    @property
    def startVerse(self) -> Verse:
        return self.__startVerse

    @property
    def endChapter(self) -> Chapter:
        return self.__endChapter

    @property
    def endVerse(self) -> Verse:
        return self.__endVerse

    def getNormalizedReferences(
        self, bible, book: str
    ) -> Iterable[NormalizedReference]:
        # here it gets tricky with chapter boundaries
        pass


class ReferenceList(list):
    def __init__(self, tokens):
        super().__init__(token for token in tokens)

    @abstractmethod
    def getNormalizedReferenceList(
        self, bible, book: str
    ) -> Iterable[NormalizedReference]:
        pass


class ChapterRangeList(ReferenceList):
    @abstractmethod
    def getNormalizedReferenceList(
        self, bible, book: str
    ) -> Iterable[NormalizedReference]:
        # here it gets tricky with chapter boundaries
        pass


class ChapterAndVerseRangeList(ReferenceList):
    def getNormalizedReferenceList(
        self, bible, book: str
    ) -> Iterable[NormalizedReference]:
        result = [
            reference
            for chapterAndVerseRangeList in self
            for reference in chapterAndVerseRangeList.getNormalizedReferences(
                bible, book
            )
        ]
        return result


class MultiChapterRangeList(ReferenceList):
    @abstractmethod
    def getNormalizedReferenceList(
        self, bible, book: str
    ) -> Iterable[NormalizedReference]:
        # here it gets tricky with chapter boundaries
        pass


class Book:
    def __init__(self, tokens):
        self.__title = tokens[0]

    @property
    def title(self) -> str:
        return self.__title

class Reference:
    __book: Book
    __chapterRangesAndVerseRanges: Union[ChapterRangeList, ChapterAndVerseRangeList, MultiChapterRangeList]

    def __init__(self, tokens):
        self.__book = tokens[0]
        self.__chapterRangesAndVerseRanges = tokens[1]

    @property
    def book(self) -> Book:
        return self.__book

    @property
    def chapterRangesAndVerseRanges(self):
        return self.__chapterRangesAndVerseRanges