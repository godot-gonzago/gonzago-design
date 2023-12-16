from pathlib import Path
from .parser import register_reader, register_writer

from gonzago.palettes.templates import Template

ID: str = "hex"
SUFFIX: str = ".hex"
DESCRIPTION = "Simple HEX color palette."


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
    colors: list[str] = []
    for entry in template.colors:
        c = entry.color.as_rgb_tuple()
        colors.append(f"{c[0]:02x}{c[1]:02x}{c[2]:02x}")
    with file.open("w") as f:
        f.writelines("\n".join(colors))


register_reader(ID, SUFFIX, DESCRIPTION, can_handle_id, can_read, read)
register_writer(
    ID, SUFFIX, DESCRIPTION, can_handle_id, change_path_from_id, can_write, write
)
