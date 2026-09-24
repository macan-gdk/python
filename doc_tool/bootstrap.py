"""Bootstrap đường dẫn project + .packages (Linux/Windows)."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PACKAGES_DIR = ROOT / ".packages"
OCR_ENV_DIR = ROOT / ".ocr-env"
DATA_DIR = ROOT / "data"


def ensure_packages_on_path() -> None:
    if PACKAGES_DIR.is_dir() and str(PACKAGES_DIR) not in sys.path:
        sys.path.insert(0, str(PACKAGES_DIR))


ensure_packages_on_path()
