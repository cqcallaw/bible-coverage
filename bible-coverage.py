from bibles.nasb.nasb1971 import bible

bible = bible.parse()

for book in bible.books:
    for chapter in book.chapters:
        for verse in chapter.verses:
            print (f"{book.name} {chapter.number}:{verse.number}")

