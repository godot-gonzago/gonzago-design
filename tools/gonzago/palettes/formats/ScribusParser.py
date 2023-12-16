from pathlib import Path

from ..core import Palette
from ..io import register_reader, register_writer

# https://github.com/1j01/anypalette.js

ID: str = "scribus"
PATTERN: str = "*.xml"
SUFFIX: str = ".xml"
DESCRIPTION = "Color palette for Scribus."


def read(file: Path) -> Palette:
    raise NotImplementedError()


def write(id: str, file: Path, palette: Palette) -> None:
    raise NotImplementedError()


register_reader(ID, PATTERN, DESCRIPTION, read)
register_writer(ID, SUFFIX, DESCRIPTION, write)
