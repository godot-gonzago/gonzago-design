from pathlib import Path
from .parser import register_reader, register_writer

from ..templates import Template

# https://docs.krita.org/en/untranslatable_pages/kpl_defintion.html


ID: str = "krita"
PATTERN: str = "*.kpl"
SUFFIX: str = ".kpl"
DESCRIPTION = "Krita color palette."


def read(file: Path) -> Template:
    raise NotImplementedError()


def write(id: str, file: Path, template: Template) -> None:
    raise NotImplementedError()


register_reader(ID, PATTERN, DESCRIPTION, read)
register_writer(ID, SUFFIX, DESCRIPTION, write)
