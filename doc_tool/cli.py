"""CLI: python -m doc_tool.cli <file> [out] [--pages N] [--layout text|visual]."""

from __future__ import annotations

import argparse
import sys

from doc_tool.export import export_attachment


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Đọc PDF/Word/Excel và xuất txt/docx (OCR tiếng Việt)."
    )
    p.add_argument("input", help="File nguồn")
    p.add_argument(
        "output",
        nargs="?",
        default=None,
        help="File đích (.docx hoặc .txt). Mặc định: cùng tên .docx",
    )
    p.add_argument(
        "--pages",
        type=int,
        default=None,
        metavar="N",
        help="Giới hạn số trang PDF",
    )
    p.add_argument(
        "--layout",
        choices=("text", "visual"),
        default="text",
        help="text=OCR sửa được; visual=ảnh trang trong Word",
    )
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    def on_progress(current: int, total: int) -> None:
        label = "Render" if args.layout == "visual" else "OCR"
        print(
            f"\r{label} trang {current}/{total}...",
            end="",
            flush=True,
            file=sys.stderr,
        )

    print(f"Đang xuất (layout={args.layout})...", file=sys.stderr)
    result = export_attachment(
        args.input,
        args.output,
        use_ocr=True,
        max_pages=args.pages,
        progress=on_progress,
        layout=args.layout,
    )
    print(file=sys.stderr)

    if result is None:
        print("(File không có text có thể đọc được)")
        return 2
    print(f"Đã ghi: {result}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
