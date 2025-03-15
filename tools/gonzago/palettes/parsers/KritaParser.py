from pathlib import Path

from ..models import Palette
from ..parsing import _register_reader, _register_writer

# https://docs.krita.org/en/untranslatable_pages/kpl_defintion.html


ID: str = "krita"
PATTERN: str = "*.kpl"
SUFFIX: str = ".kpl"
DESCRIPTION = "Krita color palette."


def read(file: Path) -> Palette:
    raise NotImplementedError()


def validate(file: Path) -> bool:
    raise NotImplementedError()


def write(palette: Palette, file: Path) -> None:
    raise NotImplementedError()


_register_reader(ID, PATTERN, DESCRIPTION, read, validate)
_register_writer(ID, SUFFIX, DESCRIPTION, write)
