from pathlib import Path

from ..models import Palette
from ..parsing import _register_reader, _register_writer

ID: str = "hex"
PATTERN: str = "*.hex"
SUFFIX: str = ".hex"
DESCRIPTION = "Simple HEX color palette."


def read(file: Path) -> Palette:
    raise NotImplementedError()


def validate(file: Path) -> bool:
    raise NotImplementedError()


def write(palette: Palette, file: Path) -> None:
    colors: list[str] = []
    for entry in palette.colors:
        c = entry.color.as_rgb_tuple()
        colors.append(f"{c[0]:02x}{c[1]:02x}{c[2]:02x}")
    with file.open("w") as f:
        f.writelines("\n".join(colors))


_register_reader(ID, PATTERN, DESCRIPTION, read, validate)
_register_writer(ID, SUFFIX, DESCRIPTION, write)
