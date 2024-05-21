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

    return Plan("RCL", [])
    # [
    #     pythonbible.convert_reference_to_verse_ids(ref)
    #     for plan_text_path in plan_text_paths
    #     for rawline in extract_text(plan_text_path).splitlines()
    #     for ref in pythonbible.get_references(
    #         text=rawline.strip(), book_groups=bible.bookgroups
    #     )
    # ],
