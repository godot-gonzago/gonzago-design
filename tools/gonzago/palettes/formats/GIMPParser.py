from pathlib import Path
from .parser import register_reader, register_writer

from gonzago.palettes.templates import Template


ID: str = "gpl"
PATTERN: str = "*/*.gpl"
SUFFIX: str = ".gpl"
DESCRIPTION = "Gimp/Inkscape color palette."


def read(file: Path) -> Template:
    raise NotImplementedError()


def write(id: str, file: Path, template: Template) -> None:
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


register_reader(ID, PATTERN, DESCRIPTION, read)
register_writer(ID, SUFFIX, DESCRIPTION, write)
