from typing import Iterable

import bible_coverage.bibles.model


class VerseRange:
    __start: int
    __end: int

    def __init__(self, tokens):
        if len(tokens) == 1:
            # single verse
            self.__start = int(tokens[0])
            self.__end = int(tokens[0])
        else:
            self.__start = int(tokens[0])
            self.__end = int(tokens[2])

    @property
    def start(self) -> int:
        return self.__start

    @property
    def end(self) -> int:
        return self.__end

    def getAllVerses(self) -> Iterable[int]:
        return (
            verse
            for verse in range(
                self.start,
                self.end + 1,  # inclusive range end
            )
        )


class VerseRangeList(list):
    def __init__(self, tokens):
        super().__init__(tokens)

    def getAllVerses(self) -> Iterable[int]:
        return (verse for verseRange in self for verse in verseRange.getAllVerses())


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


class ReferenceRangeSpecifier(list):
    def __init__(self, tokens):
        super().__init__(token for token in tokens)

    def getNormalizedReferenceList(
        self, bible, book: str
    ) -> Iterable[NormalizedReference]:
        result = [
            reference
            for chapterRangeList in self
            for reference in chapterRangeList.getNormalizedReferences(bible, book)
        ]
        return result


class ChapterRange:
    __start: int
    __end: int

    def __init__(self, tokens):
        if len(tokens) == 1:
            # single Chapter
            self.__start = tokens[0]
            self.__end = tokens[0]
        else:
            self.__start = tokens[0]
            self.__end = tokens[2]

    @property
    def start(self) -> int:
        return self.__start

    @property
    def end(self) -> int:
        return self.__end

    def getNormalizedReferences(
        self, bible: bible_coverage.bibles.model.Bible, book: str
    ) -> Iterable[NormalizedReference]:
        # range ends are incremented to make the range inclusive of the end
        if book in ["Obadiah", "2 John", "3 John", "Jude"]:
            # handle single-chapter books, where the "chapter" range is actually a verse range
            return (
                NormalizedReference(book, 1, verse)
                for verse in range(self.start, self.end + 1)  # inclusive range
            )
        else:
            return (
                NormalizedReference(book, chapter, verse)
                for chapter in range(self.start, self.end + 1)  # inclusive range
                for verse in bible.books[book][chapter].keys()
            )


class ChapterAndVerseRanges:
    __chapter: int
    __verseRanges: VerseRangeList

    def __init__(self, tokens):
        assert len(tokens) == 3
        self.__chapter = tokens[0]
        self.__verseRanges = tokens[2]

    @property
    def chapter(self) -> int:
        return self.__chapter

    @property
    def verseRanges(self) -> VerseRangeList:
        return self.__verseRanges

    def getNormalizedReferences(
        self, bible: bible_coverage.bibles.model.Bible, book: str
    ) -> Iterable[NormalizedReference]:
        return (
            NormalizedReference(book, self.chapter, verse)
            for verseRange in self.verseRanges
            for verse in verseRange.getAllVerses()
        )


class MultiChapterRange:
    __startChapter: int
    __startVerse: int
    __endChapter: int
    __endVerse: int

    def __init__(self, tokens):
        assert len(tokens) == 4
        self.__startChapter = tokens[0]
        self.__startVerse = tokens[1]
        self.__endChapter = tokens[2]
        self.__endVerse = tokens[3]

    @property
    def startChapter(self) -> int:
        return self.__startChapter

    @property
    def startVerse(self) -> int:
        return self.__startVerse

    @property
    def endChapter(self) -> int:
        return self.__endChapter

    @property
    def endVerse(self) -> int:
        return self.__endVerse

    def getNormalizedReferences(
        self, bible: bible_coverage.bibles.model.Bible, book: str
    ) -> Iterable[NormalizedReference]:
        raise Exception("unimplemented")
        return (
            NormalizedReference(book, chapter, verse)
            for chapter in range(
                self.startChapter, self.endChapter + 1
            )  # inclusive range
            for verse in range(
                self.startVerse if chapter == self.startChapter else 1,
                self.endVerse
                if chapter == self.endChapter
                else bible.books[book][chapter].keys()[-1:],
            )
        )


class WholeBookChapterRange:
    def getNormalizedReferences(
        self, bible: bible_coverage.bibles.model.Bible, book: str
    ) -> Iterable[NormalizedReference]:
        return (
            NormalizedReference(book, chapter, verse)
            for chapter in bible.books[book].keys()
            for verse in bible.books[book][chapter]
        )


class Reference:
    __book: str
    __chapterRangesAndVerseRanges: ReferenceRangeSpecifier

    def __init__(self, tokens):
        if len(tokens) == 1:
            # book reference
            self.__book = tokens[0]
            self.__chapterRangesAndVerseRanges = WholeBookChapterRange()
        else:
            assert len(tokens) == 2
            self.__book = tokens[0]
            self.__chapterRangesAndVerseRanges = tokens[1]

    @property
    def book(self) -> str:
        return self.__book

    @property
    def chapterRangesAndVerseRanges(self):
        return self.__chapterRangesAndVerseRanges
