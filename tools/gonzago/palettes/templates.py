from pathlib import Path
from typing import List, Optional

import yaml
from pydantic import BaseModel
from pydantic_extra_types.color import Color

from gonzago.pydantic import Version


TEMPLATE_FILE_PATTERN: str = "**/*.y[a]ml"


class TemplateEntry(BaseModel):
    name: str
    description: Optional[str] = None
    color: Color


class Template(BaseModel):
    name: str
    description: Optional[str] = None
    version: Optional[Version] = None
    author: Optional[str] = None
    source: Optional[str] = None
    colors: List[TemplateEntry]

    @classmethod
    def default(cls, name: str = "New Palette Template"):
        data: dict = {
            "name": name,
            "description": "A brand new palette template.",
            "version": Version(1, 0, 0),
            "author": "David Krummenacher and Gonzago Framework contributors",
            "source": "https://github.com/godot-gonzago/gonzago-design",
            "colors": [
                {
                    "name": "Black",
                    "description": "Black is an achromatic color.",
                    "color": Color("black"),
                },
                {
                    "name": "White",
                    "description": "White is an achromatic color.",
                    "color": Color("white"),
                },
            ],
        }
        return cls.model_validate(data)

    @classmethod
    def load(cls, file: Path):
        if not file.match(TEMPLATE_FILE_PATTERN) or not file.is_file():
            raise TypeError("Not a valid template path")
        with file.open() as stream:
            data: dict = yaml.safe_load(stream)
            return cls.model_validate(data)

    def save(self, file: Path) -> None:
        if not file.match(TEMPLATE_FILE_PATTERN):
            raise TypeError(f"{file} is not a valid template path")
        data: dict = Template.model_dump(self, mode="json")
        file.parent.mkdir(parents=True, exist_ok=True)  # Ensure folders
        with file.open("w") as stream:
            yaml.safe_dump(data, stream, sort_keys=False)
