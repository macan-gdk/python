"""
Facade tương thích ngược.

Ưu tiên import từ package:
  from doc_tool import export_attachment

Hoặc chạy CLI:
  python -m doc_tool.cli file.pdf out.docx --pages 2
  python index.py file.pdf out.docx --pages 2
"""

from __future__ import annotations

from doc_tool import (  # noqa: F401
    ProgressFn,
    export_attachment,
    export_to_docx,
    export_to_txt,
    read_attachment,
    read_excel,
    read_pdf,
    read_word,
)
from doc_tool.cli import main

__all__ = [
    "ProgressFn",
    "export_attachment",
    "export_to_docx",
    "export_to_txt",
    "read_attachment",
    "read_excel",
    "read_pdf",
    "read_word",
    "main",
]

if __name__ == "__main__":
    raise SystemExit(main())
