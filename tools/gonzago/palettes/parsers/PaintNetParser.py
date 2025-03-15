from pathlib import Path

from ..models import Palette
from ..parsing import _register_reader, _register_writer

ID: str = "paintnet"
PATTERN: str = "*.txt"
SUFFIX: str = ".txt"
DESCRIPTION = "Paint.NET color palette."


def read(file: Path) -> Palette:
    raise NotImplementedError()


def validate(file: Path) -> bool:
    raise NotImplementedError()


def write(palette: Palette, file: Path) -> None:
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
    raise NotImplementedError()


_register_reader(ID, PATTERN, DESCRIPTION, read, validate)
_register_writer(ID, SUFFIX, DESCRIPTION, write)
