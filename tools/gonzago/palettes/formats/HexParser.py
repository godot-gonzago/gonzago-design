from pathlib import Path
from .parser import register_reader, register_writer

from gonzago.palettes.templates import Template

ID: str = "hex"
PATTERN: str = "*/*.hex"
SUFFIX: str = ".hex"
DESCRIPTION = "Simple HEX color palette."


def read(file: Path) -> Template:
    raise NotImplementedError()


def write(id: str, file: Path, template: Template) -> None:
    colors: list[str] = []
    for entry in template.colors:
        c = entry.color.as_rgb_tuple()
        colors.append(f"{c[0]:02x}{c[1]:02x}{c[2]:02x}")
    with file.open("w") as f:
        f.writelines("\n".join(colors))


register_reader(ID, PATTERN, DESCRIPTION, read)
register_writer(ID, SUFFIX, DESCRIPTION, write)
