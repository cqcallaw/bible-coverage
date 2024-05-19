from bible_coverage.bibles.nasb.nasb1971 import bible
from bible_coverage.plans.rcl import plan

b = bible.parse()

# for book in bible.books:
#     for chapter in book.chapters:
#         for verse in chapter.verses:
#             print(f"{book.name} {chapter.number}:{verse.number}")


print("=======")
plan.parse(b)
