import os
from typing import List
from bible_coverage.model import Bible, Plan, Book, Chapter, Verse
from pdfminer.high_level import extract_text

script_dir = os.path.join(os.path.dirname(__file__))
paths = [
    os.path.join(script_dir, "RCL_YearA_Web.pdf"),
    os.path.join(script_dir, "RCL_YearB_Web.pdf"),
    os.path.join(script_dir, "RCL_YearC_Web.pdf"),
]


def parse(bible: Bible, plan_text_paths: List[str] = paths) -> Plan:
    book_names = [book.name for book in bible.books]
    textual_lines = [
        rawline.strip()
        for plan_text_path in plan_text_paths
        for rawline in extract_text(plan_text_path).splitlines()
    ]

    bible_sections = [
        line
        for line in textual_lines
        for book in bible.books
        if line.startswith(book.name)
    ]

    for bible_section in bible_sections:
        print(bible_section)

    # forms:
    # <book><chapter>
    # <book><verse range>
    # <book><chapter>:<verse range>
    # <book><chapter>:<verse range>[<optional verse range>]
    # <book><chapter>:<verse range>;<verse range>[<optional verse range>]
    # <book><chapter>:[<optional verse range>]<verse range>
    # <section> or <section>
    return Plan("RCL", [])
