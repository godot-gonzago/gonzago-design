from pathlib import Path

from ..models import Palette
from ..parsing import PaletteReader, PaletteWriter

ID: str = "hex"
PATTERN: str = "*.hex"
SUFFIX: str = ".hex"
DESCRIPTION = "Simple HEX color palette."
INTERNAL = False


class HexPaletteReader(PaletteReader):
    def read(self, file: Path) -> Palette:
        raise NotImplementedError()

    def validate(self, file: Path) -> bool:
        raise NotImplementedError()


class HexPaletteWriter(PaletteWriter):
    def write(self, palette: Palette, file: Path) -> None:
        colors: list[str] = []
        for entry in palette.colors:
            c = entry.color.as_rgb_tuple()
            colors.append(f"{c[0]:02x}{c[1]:02x}{c[2]:02x}")
        with file.open("w") as f:
            f.writelines("\n".join(colors))


PaletteReader._register_reader(
    HexPaletteReader(id=ID, description=DESCRIPTION, pattern=PATTERN, internal=INTERNAL)
)
PaletteWriter._register_writer(
    HexPaletteWriter(id=ID, description=DESCRIPTION, suffix=SUFFIX, internal=INTERNAL)
)
