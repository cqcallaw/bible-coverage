import unittest

import bible_coverage.cfg as cfg


class TestStringMethods(unittest.TestCase):
    def test_genesis(self) -> None:
        result = cfg.parse("Genesis 1:1")
        self.assertTrue(result)


if __name__ == "__main__":
    unittest.main()
