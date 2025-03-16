from pathlib import Path

from ..models import Palette
from . import PaletteReader, PaletteWriter

# https://github.com/1j01/anypalette.js

ID: str = "scribus"
PATTERN: str = "*.xml"
SUFFIX: str = ".xml"
DESCRIPTION = "Color palette for Scribus."
INTERNAL = False


class ScribusPaletteReader(PaletteReader):
    def read(self, file: Path) -> Palette:
        raise NotImplementedError()

    def validate(self, file: Path) -> bool:
        raise NotImplementedError()


class ScribusPaletteWriter(PaletteWriter):
    def write(self, palette: Palette, file: Path) -> None:
        raise NotImplementedError()


PaletteReader._register_reader(
    ScribusPaletteReader(
        id=ID, description=DESCRIPTION, pattern=PATTERN, internal=INTERNAL
    )
)
PaletteWriter._register_writer(
    ScribusPaletteWriter(
        id=ID, description=DESCRIPTION, suffix=SUFFIX, internal=INTERNAL
    )
)
