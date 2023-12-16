from pathlib import Path
from .parser import register_reader, register_writer

from gonzago.palettes.templates import Template

# https://github.com/1j01/anypalette.js

ID: str = "scribus"
SUFFIX: str = ".xml"
DESCRIPTION = "Color palette for Scribus."


def can_handle_id(id: str) -> bool:
    raise NotImplementedError()


def can_read(file: Path) -> bool:
    raise NotImplementedError()


def read(file: Path) -> Template:
    raise NotImplementedError()


def change_path_from_id(id: str, file: Path) -> Path:
    raise NotImplementedError()


def can_write(file: Path) -> bool:
    raise NotImplementedError()


def write(file: Path, template: Template) -> None:
    raise NotImplementedError()


#register_reader(ID, SUFFIX, DESCRIPTION, can_handle_id, can_read, read)
#register_writer(
#    ID, SUFFIX, DESCRIPTION, can_handle_id, change_path_from_id, can_write, write
#)
