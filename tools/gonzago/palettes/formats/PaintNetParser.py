from pathlib import Path
from .parser import register_reader, register_writer

from gonzago.palettes.templates import Template


ID: str = "paintnet"
SUFFIX: str = ".txt"
DESCRIPTION = "Paint.NET color palette."


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


#register_reader(ID, SUFFIX, DESCRIPTION, can_handle_id, can_read, read)
#register_writer(
#    ID, SUFFIX, DESCRIPTION, can_handle_id, change_path_from_id, can_write, write
#)
