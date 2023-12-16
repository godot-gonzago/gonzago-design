from pathlib import Path
from .parser import register_reader, register_writer

from gonzago.palettes.templates import Template

ID: str = "paintshop"
SUFFIX: str = ".pal"
DESCRIPTION = "Paintshop Pro color palette."


def can_handle_id(id: str) -> bool:
    raise NotImplementedError()


def can_read(file: Path) -> bool:
    raise NotImplementedError()


def read(file: Path) -> Template:
    raise NotImplementedError()


def change_path_from_id(id: str, file: Path) -> Path:
    raise NotImplementedError()


def can_write(file: Path) -> bool:
    raise NotImplementedError()


def write(file: Path, template: Template) -> None:
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


#register_reader(ID, SUFFIX, DESCRIPTION, can_handle_id, can_read, read)
#register_writer(
#    ID, SUFFIX, DESCRIPTION, can_handle_id, change_path_from_id, can_write, write
#)
