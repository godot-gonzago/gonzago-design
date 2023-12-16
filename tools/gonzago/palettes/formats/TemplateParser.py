from pathlib import Path

import yaml
from .parser import register_reader, register_writer

from gonzago.palettes.templates import Template


ID: str = "template"
PATTERN: str = "*/*.y[a]ml"
SUFFIX: str = ".yaml"
DESCRIPTION = "Gonzago palette template."


def read(id: str, file: Path) -> Template:
    if not file.match(PATTERN) or not file.is_file():
        raise TypeError(f"{file} is not a valid template path")
    with file.open() as stream:
        data: dict = yaml.safe_load(stream)
        return Template.model_validate(data)


def write(id: str, file: Path, template: Template) -> None:
    if not file.match(PATTERN):
        raise TypeError(f"{file} is not a valid template path")
    data: dict = Template.model_dump(mode="json")
    file.parent.mkdir(parents=True, exist_ok=True)  # Ensure folders
    with file.open("w") as stream:
        yaml.safe_dump(data, stream, sort_keys=False)


register_reader(ID, PATTERN, DESCRIPTION, read, False)
register_writer(ID, SUFFIX, DESCRIPTION, write, False)
