from pathlib import Path

from ..models import Palette
from ..parsing import PaletteReader, PaletteWriter

ID: str = "paintnet"
PATTERN: str = "*.txt"
SUFFIX: str = ".txt"
DESCRIPTION = "Paint.NET color palette."
INTERNAL = False


class PaintNetPaletteReader(PaletteReader):
    def read(self, file: Path) -> Palette:
        raise NotImplementedError()

    def validate(self, file: Path) -> bool:
        raise NotImplementedError()


class PaintNetPaletteWriter(PaletteWriter):
    def write(self, palette: Palette, file: Path) -> None:
        raise NotImplementedError()

    #   # https://www.getpaint.net/doc/latest/WorkingWithPalettes.html
    #   with out_file.open("w") as file:
    #        file.write(";paint.net Palette File\n")
    #        file.write(f";Palette Name: {template.name}\n")
    #        if template.description:
    #            file.write(f";Description: {template.description}\n")
    #        if template.version:
    #            file.write(f";Version: {template.version}\n")
    #        if template.author:
    #            file.write(f";Author: {template.author}\n")
    #        if template.source:
    #            file.write(f";Source: {template.source}\n")
    #        file.write(f";Colors: {len(template.colors)}\n")
    #
    #        colors: List[str] = []
    #        for entry in template.colors:
    #            c = entry.color.as_rgb_tuple()
    #            colors.append(f"FF{c[0]:02X}{c[1]:02X}{c[2]:02X}")
    #        with out_file.open("w") as file:
    #            file.writelines("\n".join(colors))


PaletteReader._register_reader(
    PaintNetPaletteReader(
        id=ID, description=DESCRIPTION, pattern=PATTERN, internal=INTERNAL
    )
)
PaletteWriter._register_writer(
    PaintNetPaletteWriter(
        id=ID, description=DESCRIPTION, suffix=SUFFIX, internal=INTERNAL
    )
)
