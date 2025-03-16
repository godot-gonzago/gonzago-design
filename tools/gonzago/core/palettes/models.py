from __future__ import annotations

import getpass
from datetime import date as Date
from enum import IntEnum
from typing import Annotated, List, Optional

from pydantic import BaseModel, Field, StringConstraints
from pydantic_extra_types.color import Color
from pydantic_extra_types.language_code import LanguageAlpha2
from pydantic_extra_types.semantic_version import SemanticVersion as Version


class GenerationDepth(IntEnum):
    MINIMAL = 1
    BASIC = 2
    ADVANCED = 3
    FULL = 4


class PaletteEntry(BaseModel):
    name: Annotated[str, StringConstraints(min_length=1)]
    description: Annotated[Optional[str], StringConstraints(min_length=1)] = None
    color: Color
    mapped_color: Optional[Color] = None


# Dublin Core Metadata
# https://www.dublincore.org/specifications/dublin-core/dcmi-terms/#section-3
class Palette(BaseModel):
    title: Annotated[str, StringConstraints(min_length=1)]
    description: Annotated[Optional[str], StringConstraints(min_length=1)] = None
    version: Optional[Version] = None
    date: Optional[Date] = None
    language: Optional[LanguageAlpha2] = None
    identifier: Annotated[
        Optional[str], StringConstraints(pattern=r"^\w*(?:\.\w*)*$")
    ] = None
    subject: Optional[List[str]] = None
    relation: Optional[str] = None
    source: Optional[str] = None
    publisher: Optional[str] = None
    creator: Optional[str] = None
    contributor: Optional[List[str]] = None
    rights: Optional[str] = None
    license: Optional[str] = None
    coverage: Optional[str] = None
    colors: Annotated[List[PaletteEntry], Field(min_length=1, default_factory=list)]
    mapped_title: Annotated[Optional[str], StringConstraints(min_length=1)] = None
    mapped_description: Annotated[Optional[str], StringConstraints(min_length=1)] = None
    mapped_suffix: Annotated[
        Optional[str],
        StringConstraints(
            min_length=1, pattern=r"^[a-z]+(?:\_[a-z]+)*(?:\.[a-z]+(?:\_[a-z]+)*)*$"
        ),
    ] = None

    @staticmethod
    def generate_default(
        title: str, depth: GenerationDepth = GenerationDepth.BASIC
    ) -> Palette:
        if not title:
            title = "New Palette Template"

        black: PaletteEntry = PaletteEntry(name="Black", color=Color("black"))
        white: PaletteEntry = PaletteEntry(name="White", color=Color("white"))

        palette: Palette = Palette(title=title, colors=[black, white])

        if depth.value < GenerationDepth.BASIC.value:
            return palette

        palette.description = "A brand new palette template."
        palette.version = Version(1, 0, 0)
        palette.source = "https://github.com/godot-gonzago"
        palette.publisher = "Gonzago Framework"
        palette.creator = getpass.getuser()
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
