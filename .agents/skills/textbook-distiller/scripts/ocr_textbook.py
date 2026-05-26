"""OCR a textbook PDF into page-level Markdown and JSONL evidence files.

The script is intentionally generic: it does not know any course-specific
chapter names. It renders pages with PyMuPDF and recognizes text with
rapidocr-onnxruntime.
"""

from __future__ import annotations

import argparse
import json
import statistics
import tempfile
from datetime import datetime
from pathlib import Path

import fitz
from rapidocr_onnxruntime import RapidOCR
from tqdm import tqdm


def parse_pages(spec: str | None, total: int) -> list[int]:
    if not spec:
        return list(range(1, total + 1))

    pages: set[int] = set()
    for part in spec.split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            start_s, end_s = part.split("-", 1)
            start, end = int(start_s), int(end_s)
            pages.update(range(start, end + 1))
        else:
            pages.add(int(part))

    return [p for p in sorted(pages) if 1 <= p <= total]


def line_to_record(item: list) -> dict:
    box, text, score = item[0], item[1], item[2]
    return {
        "text": str(text).strip(),
        "confidence": float(score),
        "box": box,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="OCR a textbook PDF page by page.")
    parser.add_argument("--pdf", required=True, help="Path to the source PDF.")
    parser.add_argument("--out-dir", required=True, help="Output directory.")
    parser.add_argument("--pages", help="Page spec such as 1-10,15,20-25. Defaults to all pages.")
    parser.add_argument("--zoom", type=float, default=2.0, help="Render zoom. 2.0 is a good default.")
    parser.add_argument("--keep-images", action="store_true", help="Keep rendered page images.")
    parser.add_argument("--min-confidence", type=float, default=0.60, help="Low confidence threshold.")
    parser.add_argument("--resume", action="store_true", help="Skip pages whose Markdown and JSONL outputs already exist.")
    args = parser.parse_args()

    pdf = Path(args.pdf)
    out_dir = Path(args.out_dir)
    pages_dir = out_dir / "pages"
    jsonl_dir = out_dir / "jsonl"
    image_dir = out_dir / "images"
    pages_dir.mkdir(parents=True, exist_ok=True)
    jsonl_dir.mkdir(parents=True, exist_ok=True)
    if args.keep_images:
        image_dir.mkdir(parents=True, exist_ok=True)

    doc = fitz.open(str(pdf))
    selected_pages = parse_pages(args.pages, doc.page_count)
    ocr = RapidOCR()
    manifest_pages: list[dict] = []
    all_confidences: list[float] = []
    low_confidence_count = 0

    with tempfile.TemporaryDirectory() as tmp:
        tmp_dir = Path(tmp)
        for page_no in tqdm(selected_pages, desc="OCR pages"):
            md_path = pages_dir / f"page-{page_no:03d}.md"
            jsonl_path = jsonl_dir / f"page-{page_no:03d}.jsonl"
            if args.resume and md_path.exists() and jsonl_path.exists():
                manifest_pages.append(
                    {
                        "pdf_page": page_no,
                        "markdown": str(md_path.as_posix()),
                        "jsonl": str(jsonl_path.as_posix()),
                        "line_count": None,
                        "mean_confidence": None,
                        "low_confidence_lines": None,
                        "elapsed": "skipped",
                    }
                )
                continue

            page = doc[page_no - 1]
            pix = page.get_pixmap(matrix=fitz.Matrix(args.zoom, args.zoom), alpha=False)
            image_path = (image_dir if args.keep_images else tmp_dir) / f"page-{page_no:03d}.png"
            pix.save(str(image_path))

            result, elapsed = ocr(str(image_path))
            records = [line_to_record(item) for item in (result or []) if str(item[1]).strip()]
            text_lines = [r["text"] for r in records]
            confidences = [r["confidence"] for r in records]
            all_confidences.extend(confidences)
            page_low = sum(1 for score in confidences if score < args.min_confidence)
            low_confidence_count += page_low

            md_path.write_text(
                "\n".join(
                    [
                        f"# Page {page_no}",
                        "",
                        f"- source_pdf: `{pdf.name}`",
                        f"- pdf_page: {page_no}",
                        f"- line_count: {len(records)}",
                        f"- mean_confidence: {statistics.mean(confidences):.4f}" if confidences else "- mean_confidence: 0",
                        f"- low_confidence_lines: {page_low}",
                        "",
                        "## OCR Text",
                        "",
                        "\n".join(text_lines),
                        "",
                    ]
                ),
                encoding="utf-8",
            )
            with jsonl_path.open("w", encoding="utf-8") as f:
                for record in records:
                    f.write(json.dumps(record, ensure_ascii=False) + "\n")

            manifest_pages.append(
                {
                    "pdf_page": page_no,
                    "markdown": str(md_path.as_posix()),
                    "jsonl": str(jsonl_path.as_posix()),
                    "line_count": len(records),
                    "mean_confidence": statistics.mean(confidences) if confidences else 0,
                    "low_confidence_lines": page_low,
                    "elapsed": elapsed,
                }
            )

    manifest = {
        "source_pdf": str(pdf),
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "page_count": doc.page_count,
        "processed_pages": len(selected_pages),
        "page_spec": args.pages or "all",
        "zoom": args.zoom,
        "min_confidence": args.min_confidence,
        "mean_confidence": statistics.mean(all_confidences) if all_confidences else 0,
        "low_confidence_lines": low_confidence_count,
        "pages": manifest_pages,
    }
    (out_dir / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")

    summary = [
        "# OCR 运行摘要",
        "",
        f"- 源文件：`{pdf.name}`",
        f"- PDF 页数：{doc.page_count}",
        f"- 已处理页数：{len(selected_pages)}",
        f"- 页面范围：{args.pages or 'all'}",
        f"- 平均置信度：{manifest['mean_confidence']:.4f}",
        f"- 低置信度文本行数：{low_confidence_count}",
        "",
        "## 说明",
        "",
        "低置信度文本行、公式、表格和图示仍需人工复核；本文件只记录 OCR 运行结果。",
        "",
    ]
    (out_dir / "ocr-summary.md").write_text("\n".join(summary), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
