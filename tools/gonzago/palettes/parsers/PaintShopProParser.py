from pathlib import Path

from ..models import Palette
from ..parsing import register_reader, register_writer

ID: str = "paintshop"
PATTERN: str = "*.pal"
SUFFIX: str = ".pal"
DESCRIPTION = "Paintshop Pro color palette."


def read(file: Path) -> Palette:
    raise NotImplementedError()


def validate(file: Path) -> bool:
    raise NotImplementedError()


def write(palette: Palette, file: Path) -> None:
    #    # https://liero.nl/lierohack/docformats/other-jasc.html
    #    # JASC-PAL      <- constant string
    #    # 0100          <- constant version of palette file format
    #    # 16            <- color count
    #    # 255 0 0       <- [0-255] rgb separated by space
    #    # 0 255 0
    #    # 0 0 255
    #    # 255 255 0
    #    pass
    raise NotImplementedError()


register_reader(ID, PATTERN, DESCRIPTION, read, validate)
register_writer(ID, SUFFIX, DESCRIPTION, write)
