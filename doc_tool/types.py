"""Kiểu dùng chung."""

from __future__ import annotations

from typing import Callable

# progress(current_page, total_pages)
ProgressFn = Callable[[int, int], None]
