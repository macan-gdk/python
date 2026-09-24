"""Tìm và cấu hình Tesseract trên Ubuntu / Windows."""

from __future__ import annotations

import os
import shutil
from pathlib import Path

from doc_tool.bootstrap import OCR_ENV_DIR


def _candidate_cmds() -> list[Path]:
    found: list[Path] = []
    exe = "tesseract.exe" if os.name == "nt" else "tesseract"
    found.append(OCR_ENV_DIR / "bin" / exe)

    which = shutil.which("tesseract")
    if which:
        found.append(Path(which))

    if os.name == "nt":
        pf = os.environ.get("ProgramFiles", r"C:\Program Files")
        pf86 = os.environ.get("ProgramFiles(x86)", r"C:\Program Files (x86)")
        local = os.environ.get("LOCALAPPDATA", "")
        found.append(Path(pf) / "Tesseract-OCR" / "tesseract.exe")
        found.append(Path(pf86) / "Tesseract-OCR" / "tesseract.exe")
        if local:
            found.append(Path(local) / "Programs" / "Tesseract-OCR" / "tesseract.exe")
    else:
        found.extend([Path("/usr/bin/tesseract"), Path("/usr/local/bin/tesseract")])
    return found


def _candidate_tessdata(tesseract_cmd: Path) -> list[Path]:
    dirs = [
        OCR_ENV_DIR / "share" / "tessdata",
        tesseract_cmd.parent / "tessdata",
        Path("/usr/share/tesseract-ocr/5/tessdata"),
        Path("/usr/share/tesseract-ocr/4.00/tessdata"),
        Path("/usr/share/tessdata"),
    ]
    env = os.environ.get("TESSDATA_PREFIX")
    if env:
        dirs.insert(0, Path(env))
    return dirs


def configure_tesseract() -> bool:
    """
    Trỏ pytesseract tới binary + tessdata.
    True nếu tìm thấy tesseract; False nếu không (caller có thể fallback).
    """
    from pytesseract import pytesseract as tess_mod

    cmd = next((c for c in _candidate_cmds() if c.is_file()), None)
    if cmd is None:
        return False

    tess_mod.tesseract_cmd = str(cmd)
    for data_dir in _candidate_tessdata(cmd):
        if not data_dir.is_dir():
            continue
        if (data_dir / "vie.traineddata").is_file() or (
            data_dir / "eng.traineddata"
        ).is_file():
            os.environ["TESSDATA_PREFIX"] = str(data_dir)
            break
    return True
