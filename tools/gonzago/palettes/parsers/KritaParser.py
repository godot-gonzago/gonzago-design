from pathlib import Path

from ..models import Palette
from ..parsing import PaletteReader, PaletteWriter

# https://docs.krita.org/en/untranslatable_pages/kpl_defintion.html


ID: str = "krita"
PATTERN: str = "*.kpl"
SUFFIX: str = ".kpl"
DESCRIPTION = "Krita color palette."
INTERNAL = False


class KritaPaletteReader(PaletteReader):
    def read(self, file: Path) -> Palette:
        raise NotImplementedError()

    def validate(self, file: Path) -> bool:
        raise NotImplementedError()


class KritaPaletteWriter(PaletteWriter):
    def write(self, palette: Palette, file: Path) -> None:
        raise NotImplementedError()


PaletteReader._register_reader(
    KritaPaletteReader(
        id=ID, description=DESCRIPTION, pattern=PATTERN, internal=INTERNAL
    )
)
PaletteWriter._register_writer(
    KritaPaletteWriter(id=ID, description=DESCRIPTION, suffix=SUFFIX, internal=INTERNAL)
)
