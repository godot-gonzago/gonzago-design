from pathlib import Path

from ..core import Palette, register_reader, register_writer

# https://github.com/1j01/anypalette.js

ID: str = "scribus"
PATTERN: str = "*.xml"
SUFFIX: str = ".xml"
DESCRIPTION = "Color palette for Scribus."


def read(file: Path) -> Palette:
    raise NotImplementedError()


def validate(file: Path) -> bool:
    raise NotImplementedError()


def write(palette: Palette, file: Path) -> None:
    raise NotImplementedError()


register_reader(ID, PATTERN, DESCRIPTION, read, validate)
register_writer(ID, SUFFIX, DESCRIPTION, write)
