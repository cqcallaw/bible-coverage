import unittest

import pyparsing
import pytest

import bible_coverage.cfg as cfg


# forms:
# <book><chapter>
# <book><verse range>
# <book><chapter>:<verse range>
# <book><chapter>:<verse range>[<optional verse range>]
# <book><chapter>:<verse range>;<verse range>[<optional verse range>]
# <book><chapter>:[<optional verse range>]<verse range>
# <section> or <section>


class TestVerseParsing(unittest.TestCase):
    def test_genesis(self) -> None:
        result = cfg.parse("Genesis 1:1")
        assert result
        self.assertEqual(result.book, "Genesis")
        self.assertEqual(result.chapter, "1")
        self.assertEqual(result.start_verse, "1")

    def test_whole_psalm(self) -> None:
        result = cfg.parse("Psalm 100")
        assert result
        self.assertEqual(result.book, "Psalm")
        self.assertEqual(result.chapter, "100")
        self.assertFalse(result.start_verse)

    def test_whole_book(self) -> None:
        result = cfg.parse("Jude")
        assert result
        self.assertEqual(result.book, "Jude")
        self.assertFalse(result.chapter)
        self.assertFalse(result.start_verse)

    def test_short_book_verse(self) -> None:
        result = cfg.parse("Jude 3")
        assert result
        self.assertEqual(result.book, "Jude")
        self.assertFalse(result.chapter)
        self.assertEqual(result.start_verse, "3")

    def test_invalid(self) -> None:
        with pytest.raises(pyparsing.exceptions.ParseException):
            result = cfg.parse("Enoch 1:1")

    def test_basic_range(self) -> None:
        result = cfg.parse("Genesis 15:1-6")
        assert result
        self.assertEqual(result.book, "Genesis")
        self.assertEqual(result.chapter, "15")
        self.assertEqual(result.start_verse, "1")
        self.assertEqual(result.end_verse, "6")


if __name__ == "__main__":
    unittest.main()
