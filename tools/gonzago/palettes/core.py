from datetime import date as Date
from enum import Enum
from typing import List, Optional, Set

from pydantic import BaseModel, Field, conlist, constr
from pydantic_extra_types.color import Color

from ..pydantic import Version


class PaletteEntry(BaseModel):
    name: constr(min_length=1)
    description: Optional[str] = None
    color: Color


# Dublin Core Metadata
# https://www.dublincore.org/specifications/dublin-core/dcmi-terms/#section-3
class Palette(BaseModel):
    title: constr(min_length=1)
    description: Optional[str] = None
    version: Optional[Version] = None
    date: Optional[Date] = None
    language: Optional[str] = None
    identifier: Optional[str] = None
    subject: Optional[Set[str]] = None
    relation: Optional[str] = None
    source: Optional[str] = None
    publisher: Optional[str] = None
    creator: Optional[str] = None
    contributor: Optional[List[str]] = None
    rights: Optional[str] = None
    license: Optional[str] = None
    coverage: Optional[str] = None
    colors: conlist(PaletteEntry, min_length=1)


class GenerationDepth(Enum):
    MINIMAL = 1
    BASIC = 2
    ADVANCED = 3
    FULL = 4


def generate_default_palette(
    title: str, depth: GenerationDepth = GenerationDepth.BASIC
) -> Palette:
    if not title:
        title = "New Palette Template"

    black = PaletteEntry(name="Black", color=Color("black"))
    white = PaletteEntry(name="White", color=Color("white"))
    palette = Palette(title=title, colors=[black, white])
    if depth.value < GenerationDepth.BASIC.value:
        return palette

    palette.description = "A brand new palette template."
    palette.version = Version(1, 0, 0)
    palette.source = "https://github.com/godot-gonzago"
    palette.publisher = "Gonzago Framework"
    palette.creator = "David Krummenacher"
    black.description = "Black is an achromatic color."
    white.description = "White is an achromatic color."
    if depth.value < GenerationDepth.ADVANCED.value:
        return palette

    palette.date = Date.today()
    palette.language = "en"
    palette.identifier = "gonzago.palettes.new"
    if depth.value < GenerationDepth.FULL.value:
        return palette

    palette.subject = ["gonzago", "palette", "new"]
    palette.relation = "https://www.w3.org/wiki/CSS/Properties/color/keywords"
    palette.contributor = ["David Krummenacher"]
    palette.rights = (
        "Copyright (c) 2023 David Krummenacher and Gonzago Framework contributors"
    )
    palette.license = "http://creativecommons.org/licenses/by/4.0/"
    palette.coverage = "Global"
    return palette
