from pathlib import Path

import yaml
from ..io import Palette, register_reader, register_writer


ID: str = "template"
PATTERN: str = "*.yaml"
SUFFIX: str = ".yaml"
DESCRIPTION = "Gonzago palette template."


def read(file: Path) -> Palette:
    if not file.match(PATTERN) or not file.is_file():
        raise TypeError(f"{file} is not a valid template path")
    with file.open() as stream:
        data: dict = yaml.safe_load(stream)
        return Palette.model_validate(data)


def write(id: str, file: Path, palette: Palette) -> None:
    if not file.match(PATTERN):
        raise TypeError(f"{file} is not a valid template path")
    data: dict = Palette.model_dump(mode="json")
    file.parent.mkdir(parents=True, exist_ok=True)  # Ensure folders
    with file.open("w") as stream:
        yaml.safe_dump(data, stream, sort_keys=False)


register_reader(ID, PATTERN, DESCRIPTION, read)
register_writer(ID, SUFFIX, DESCRIPTION, write, False)
