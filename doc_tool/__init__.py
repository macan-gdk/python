"""
doc_tool — đọc file đính kèm (PDF/Word/Excel) và xuất txt/docx.

Public API dùng cho UI / script:
  from doc_tool import export_attachment, read_attachment
"""

from __future__ import annotations

from doc_tool.bootstrap import ensure_packages_on_path

ensure_packages_on_path()

from doc_tool.export import (  # noqa: E402
    export_attachment,
    export_to_docx,
    export_to_txt,
)
from doc_tool.readers import (  # noqa: E402
    read_attachment,
    read_excel,
    read_pdf,
    read_word,
)
from doc_tool.types import ProgressFn  # noqa: E402

__all__ = [
    "ProgressFn",
    "export_attachment",
    "export_to_docx",
    "export_to_txt",
    "read_attachment",
    "read_excel",
    "read_pdf",
    "read_word",
]
