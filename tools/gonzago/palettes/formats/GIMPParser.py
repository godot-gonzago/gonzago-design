from pathlib import Path
from .parser import register_reader, register_writer

from gonzago.palettes.templates import Template


ID: str = "gpl"
SUFFIX: str = ".gpl"
DESCRIPTION = "Gimp/Inkscape color palette."


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
    with file.open("w") as f:
        f.write("GIMP Palette\n")
        f.write(f"Name: {template.name}\n")
        f.write(f"Columns: 0\n")

        if template.description:
            f.write(f"# Description: {template.description}\n")
        if template.version:
            f.write(f"# Version: {template.version}\n")
        if template.author:
            f.write(f"# Author: {template.author}\n")
        if template.source:
            f.write(f"# Source: {template.source}\n")

        f.write(f"#")

        for entry in template.colors:
            c = entry.color.as_rgb_tuple()
            f.write(f"\n{c[0]:d}\t{c[1]:d}\t{c[2]:d}\t{entry.name}")
            if entry.description:
                f.write(f" - {entry.description}")


register_reader(ID, SUFFIX, DESCRIPTION, can_handle_id, can_read, read)
register_writer(
    ID, SUFFIX, DESCRIPTION, can_handle_id, change_path_from_id, can_write, write
)
