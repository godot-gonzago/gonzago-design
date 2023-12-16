from pathlib import Path
from .parser import register_reader, register_writer

from ..templates import Template

ID: str = "paintshop"
PATTERN: str = "*/*.pal"
SUFFIX: str = ".pal"
DESCRIPTION = "Paintshop Pro color palette."


def read(file: Path) -> Template:
    raise NotImplementedError()


def write(id: str, file: Path, template: Template) -> None:
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


register_reader(ID, PATTERN, DESCRIPTION, read)
register_writer(ID, SUFFIX, DESCRIPTION, write)
