from pathlib import Path
from .parser import register_reader, register_writer

from ..templates import Template

# https://github.com/1j01/anypalette.js

ID: str = "scribus"
PATTERN: str = "*.xml"
SUFFIX: str = ".xml"
DESCRIPTION = "Color palette for Scribus."


def read(file: Path) -> Template:
    raise NotImplementedError()


def write(id: str, file: Path, template: Template) -> None:
    raise NotImplementedError()


register_reader(ID, PATTERN, DESCRIPTION, read)
register_writer(ID, SUFFIX, DESCRIPTION, write)
