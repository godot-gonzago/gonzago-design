from pathlib import Path

from ..core import Palette
from ..io import register_reader, register_writer

# https://docs.krita.org/en/untranslatable_pages/kpl_defintion.html


ID: str = "krita"
PATTERN: str = "*.kpl"
SUFFIX: str = ".kpl"
DESCRIPTION = "Krita color palette."


def read(file: Path) -> Palette:
    raise NotImplementedError()


def write(id: str, file: Path, palette: Palette) -> None:
    raise NotImplementedError()


register_reader(ID, PATTERN, DESCRIPTION, read)
register_writer(ID, SUFFIX, DESCRIPTION, write)
