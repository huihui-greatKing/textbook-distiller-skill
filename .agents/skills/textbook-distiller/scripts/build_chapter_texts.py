"""Build chapter-level OCR text bundles from page-level OCR output."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


CHAPTER_ROW = re.compile(
    r"^\|\s*(第\s*\d+\s*章|参考文献)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*(\d+)\s*-\s*(\d+)\s*\|"
)


def parse_book_structure(path: Path) -> list[dict]:
    chapters: list[dict] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        match = CHAPTER_ROW.match(line)
        if not match:
            continue
        chapter, title, body_pages, start, end = match.groups()
        chapters.append(
            {
                "chapter": " ".join(chapter.split()),
                "title": title.strip(),
                "body_pages": body_pages.strip(),
                "pdf_start": int(start),
                "pdf_end": int(end),
            }
        )
    return chapters


def slug_for(chapter: str, title: str) -> str:
    if chapter == "参考文献":
        return "references"
    num = re.search(r"\d+", chapter)
    prefix = f"chapter-{int(num.group()):02d}" if num else "chapter"
    return prefix


def read_page_text(pages_dir: Path, page_no: int) -> str:
    path = pages_dir / f"page-{page_no:03d}.md"
    if not path.exists():
        return f"[Page {page_no} OCR missing]"
    text = path.read_text(encoding="utf-8")
    marker = "## OCR Text"
    return text.split(marker, 1)[1].strip() if marker in text else text.strip()


def main() -> int:
    parser = argparse.ArgumentParser(description="Bundle OCR pages into chapter files.")
    parser.add_argument("--ocr-dir", required=True, help="Directory created by ocr_textbook.py.")
    parser.add_argument("--book-structure", required=True, help="BOOK_STRUCTURE.md path.")
    parser.add_argument("--out-dir", required=True, help="Output directory for chapter OCR bundles.")
    args = parser.parse_args()

    ocr_dir = Path(args.ocr_dir)
    pages_dir = ocr_dir / "pages"
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    manifest_path = ocr_dir / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8")) if manifest_path.exists() else {}
    chapters = parse_book_structure(Path(args.book_structure))
    index_lines = [
        "# 章节 OCR 文本索引",
        "",
        f"- OCR 来源：`{ocr_dir}`",
        f"- OCR 页面数：{manifest.get('processed_pages', '未知')}",
        "",
        "| 章次 | 标题 | PDF 页序 | 输出文件 |",
        "| --- | --- | --- | --- |",
    ]

    for chapter in chapters:
        slug = slug_for(chapter["chapter"], chapter["title"])
        out_path = out_dir / f"{slug}.md"
        page_chunks = []
        for page_no in range(chapter["pdf_start"], chapter["pdf_end"] + 1):
            page_chunks.append(f"## PDF Page {page_no}\n\n{read_page_text(pages_dir, page_no)}")
        out_path.write_text(
            "\n\n".join(
                [
                    f"# {chapter['chapter']} {chapter['title']} OCR 文本",
                    "",
                    f"- 教材正文页码：{chapter['body_pages']}",
                    f"- 完整本 PDF 物理页序：{chapter['pdf_start']}-{chapter['pdf_end']}",
                    "",
                    *page_chunks,
                    "",
                ]
            ),
            encoding="utf-8",
        )
        index_lines.append(
            f"| {chapter['chapter']} | {chapter['title']} | {chapter['pdf_start']}-{chapter['pdf_end']} | `{out_path.as_posix()}` |"
        )

    (out_dir / "index.md").write_text("\n".join(index_lines) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
