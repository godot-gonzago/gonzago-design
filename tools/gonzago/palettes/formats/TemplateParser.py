from pathlib import Path

import yaml
from .parser import register_reader, register_writer

from gonzago.palettes.templates import Template


ID: str = "template"
SUFFIX: str = ".yaml"
DESCRIPTION = "Gonzago palette template."

TEMPLATE_FILE_PATTERN: str = "*/*.y[a]ml"


def can_handle_id(id: str) -> bool:
    return id == "template"


def can_read(file: Path) -> bool:
    return file.exists() and file.match(TEMPLATE_FILE_PATTERN)


def read(file: Path) -> Template:
    if not file.match(TEMPLATE_FILE_PATTERN) or not file.is_file():
        raise TypeError(f"{file} is not a valid template path")
    with file.open() as stream:
        data: dict = yaml.safe_load(stream)
        return Template.model_validate(data)


def change_path_from_id(id: str, file: Path) -> Path:
    raise NotImplementedError()


def can_write(file: Path) -> bool:
    raise NotImplementedError()


def write(file: Path, template: Template) -> None:
    if not file.match(TEMPLATE_FILE_PATTERN):
        raise TypeError(f"{file} is not a valid template path")
    data: dict = Template.model_dump(mode="json")
    file.parent.mkdir(parents=True, exist_ok=True)  # Ensure folders
    with file.open("w") as stream:
        yaml.safe_dump(data, stream, sort_keys=False)


register_reader(ID, SUFFIX, DESCRIPTION, can_handle_id, can_read, read, False)
register_writer(
    ID, SUFFIX, DESCRIPTION, can_handle_id, change_path_from_id, can_write, write, False
)
