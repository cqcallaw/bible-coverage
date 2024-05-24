import os
import pytest

import bible_coverage.bibles.nasb.nasb1971.bible as bible


def test_genesis_1_parse() -> None:
    result = bible.parse(os.path.join(os.path.dirname(__file__), "genesis_1_nasb.txt"))
    assert "Genesis" in result.books.keys()
    assert 1 in result.books["Genesis"].keys()
    assert 1 in result.books["Genesis"][1].keys()
    assert 31 in result.books["Genesis"][1].keys()


def test_genesis_1_3_parse() -> None:
    result = bible.parse(
        os.path.join(os.path.dirname(__file__), "genesis_1-3_nasb.txt")
    )
    assert "Genesis" in result.books.keys()
    assert 1 in result.books["Genesis"].keys()
    assert 1 in result.books["Genesis"][1].keys()
    assert result.books["Genesis"][1][1]
    assert 31 in result.books["Genesis"][1].keys()
    assert 3 in result.books["Genesis"].keys()


def test_genesis_and_exodus_parse() -> None:
    result = bible.parse(
        os.path.join(os.path.dirname(__file__), "genesis+exodus_nasb.txt")
    )
    assert "Genesis" in result.books.keys()
    assert result.books["Genesis"][1][1]
    assert result.books["Genesis"][3][24]
    assert "Exodus" in result.books.keys()
    assert result.books["Exodus"][40][38]


if __name__ == "__main__":
    pytest.main()
