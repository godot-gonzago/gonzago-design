from pathlib import Path

from ..models import Palette
from ..parsing import PaletteReader, PaletteWriter

ID: str = "paintshop"
PATTERN: str = "*.pal"
SUFFIX: str = ".pal"
DESCRIPTION = "Paintshop Pro color palette."
INTERNAL = False


class PaintShopProPaletteReader(PaletteReader):
    def read(self, file: Path) -> Palette:
        raise NotImplementedError()

    def validate(self, file: Path) -> bool:
        raise NotImplementedError()


class PaintShopProPaletteWriter(PaletteWriter):
    def write(self, palette: Palette, file: Path) -> None:
        raise NotImplementedError()

    #    # https://liero.nl/lierohack/docformats/other-jasc.html
    #    # JASC-PAL      <- constant string
    #    # 0100          <- constant version of palette file format
    #    # 16            <- color count
    #    # 255 0 0       <- [0-255] rgb separated by space
    #    # 0 255 0
    #    # 0 0 255
    #    # 255 255 0
    #    pass


PaletteReader._register_reader(
    PaintShopProPaletteReader(
        id=ID, description=DESCRIPTION, pattern=PATTERN, internal=INTERNAL
    )
)
PaletteWriter._register_writer(
    PaintShopProPaletteWriter(
        id=ID, description=DESCRIPTION, suffix=SUFFIX, internal=INTERNAL
    )
)
