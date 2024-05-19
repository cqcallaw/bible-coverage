from collections import UserList
from typing import List


class Verse:
    def __init__(self, tokens):
        self.__number = int(tokens[0])

    @property
    def number(self) -> int:
        return self.__number


class VerseRange:
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


class VerseRangeList:
    def __init__(self, tokens):
        self.__ranges = tokens

    @property
    def ranges(self) -> List[VerseRange]:
        return self.__ranges


class ChapterAndVerseRanges:
    def __init__(self, tokens):
        self.__chapter = int(tokens[0])
        if len(tokens) == 3:
            self.__verseRanges = tokens[2]
        else:
            self.__verseRanges = []

    @property
    def chapter(self) -> int:
        return self.__chapter

    @property
    def verseRanges(self) -> VerseRangeList:
        return self.__verseRanges


class Reference:
    def __init__(self, tokens):
        self.book = tokens[0]
        self.chapter = tokens[1].chapter
        self.verseRanges = tokens[1].verseRanges
