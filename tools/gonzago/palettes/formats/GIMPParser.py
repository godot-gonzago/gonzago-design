from pathlib import Path

from ..core import Palette
from ..io import register_reader, register_writer


ID: str = "gpl"
PATTERN: str = "*.gpl"
SUFFIX: str = ".gpl"
DESCRIPTION = "Gimp/Inkscape color palette."


def read(file: Path) -> Palette:
    raise NotImplementedError()


def write(id: str, file: Path, palette: Palette) -> None:
    with file.open("w") as f:
        f.write("GIMP Palette\n")
        f.write(f"Name: {palette.name}\n")
        f.write(f"Columns: 0\n")

        if palette.description:
            f.write(f"# Description: {palette.description}\n")
        if palette.version:
            f.write(f"# Version: {palette.version}\n")
        if palette.author:
            f.write(f"# Author: {palette.author}\n")
        if palette.source:
            f.write(f"# Source: {palette.source}\n")

        f.write(f"#")

        for entry in palette.colors:
            c = entry.color.as_rgb_tuple()
            f.write(f"\n{c[0]:d}\t{c[1]:d}\t{c[2]:d}\t{entry.name}")
            if entry.description:
                f.write(f" - {entry.description}")


register_reader(ID, PATTERN, DESCRIPTION, read)
register_writer(ID, SUFFIX, DESCRIPTION, write)
