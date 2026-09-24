"""Type stubs for pytesseract (IDE / Pyrefly / basedpyright)."""

from __future__ import annotations

from typing import Any

class TesseractError(Exception): ...
class TesseractNotFoundError(TesseractError): ...
class TSVNotSupported(TesseractError): ...
class ALTONotSupported(TesseractError): ...

class Output:
    BYTES: str
    DATAFRAME: str
    DICT: str
    STRING: str

tesseract_cmd: str

def get_languages(config: str = ...) -> list[str]: ...
def get_tesseract_version() -> Any: ...
def image_to_string(
    image: Any,
    lang: str | None = ...,
    config: str = ...,
    nice: int = ...,
    timeout: float = ...,
) -> str: ...
def image_to_boxes(
    image: Any,
    lang: str | None = ...,
    config: str = ...,
    nice: int = ...,
    output_type: str = ...,
    timeout: float = ...,
) -> Any: ...
def image_to_data(
    image: Any,
    lang: str | None = ...,
    config: str = ...,
    nice: int = ...,
    output_type: str = ...,
    timeout: float = ...,
) -> Any: ...
def image_to_osd(
    image: Any,
    lang: str | None = ...,
    config: str = ...,
    nice: int = ...,
    output_type: str = ...,
    timeout: float = ...,
) -> Any: ...
def image_to_pdf_or_hocr(
    image: Any,
    lang: str | None = ...,
    config: str = ...,
    nice: int = ...,
    extension: str = ...,
    timeout: float = ...,
) -> bytes: ...
def image_to_alto_xml(
    image: Any,
    lang: str | None = ...,
    config: str = ...,
    nice: int = ...,
    timeout: float = ...,
) -> bytes: ...
def run_and_get_output(*args: Any, **kwargs: Any) -> Any: ...
def run_and_get_multiple_output(*args: Any, **kwargs: Any) -> Any: ...

# Submodule used as: from pytesseract import pytesseract
class pytesseract:  # noqa: N801 — mirrors real package layout
    tesseract_cmd: str
    TesseractError: type[TesseractError]
    TesseractNotFoundError: type[TesseractNotFoundError]
    def image_to_string(
        image: Any,
        lang: str | None = ...,
        config: str = ...,
        nice: int = ...,
        timeout: float = ...,
    ) -> str: ...
