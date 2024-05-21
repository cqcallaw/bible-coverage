import unittest
from bible_coverage.bibles.nasb.nasb1971 import bible
from bible_coverage.plans.rcl import plan

b = bible.parse()


class TestPlanParsing(unittest.TestCase):
    def testRCL(self) -> None:
        b = bible.parse()
        plan.parse(b)
