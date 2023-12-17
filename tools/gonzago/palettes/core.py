from datetime import date as Date
from typing import List, Optional, Set

from pydantic import BaseModel, Field, conlist, constr
from pydantic_extra_types.color import Color

from ..pydantic import Version


class PaletteEntry(BaseModel):
    name: constr(min_length=1)
    description: Optional[str] = None
    color: Color


# Dublin Core Metadata https://www.dublincore.org/specifications/dublin-core/dcmi-terms/#section-3
class Palette(BaseModel):
    title: constr(min_length=1)
    description: Optional[str] = None
    identifier: Optional[str] = None
    version: Optional[Version] = None
    date: Optional[Date] = None
    language: Optional[str] = None
    subject: Optional[Set[str]] = None
    creator: Optional[str] = None
    contributor: Optional[List[str]] = None
    publisher: Optional[str] = None
    source: Optional[str] = None
    relation: Optional[str] = None
    rights: Optional[str] = None
    license: Optional[str] = None
    coverage: Optional[str] = None
    colors: conlist(PaletteEntry, min_length=1)


def generate_default_palette(title: str) -> Palette:
    if not title:
        title = "New Palette Template"

    return Palette(
        title = title,
        description = "A brand new palette template.",
        identifier = "gonzago.palettes.new",
        version = Version(1, 0, 0),
        date = Date.today(),
        language = "en",
        subject = ["gonzago", "palette", "new"],
        creator = "David Krummenacher",
        contributor = ["David Krummenacher"],
        publisher = "Gonzago Framework",
        source = "https://github.com/godot-gonzago",
        rights = "Copyright (c) 2023 David Krummenacher and Gonzago Framework contributors",
        license = "http://creativecommons.org/licenses/by/4.0/",
        colors = [
            PaletteEntry(
                name="Black",
                description="Black is an achromatic color.",
                color=Color("black")
            ),
            PaletteEntry(
                name="White",
                description="White is an achromatic color.",
                color=Color("white")
            )
        ]
    )
