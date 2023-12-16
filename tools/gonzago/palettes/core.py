from typing import List, Optional

from pydantic import BaseModel
from pydantic_extra_types.color import Color

from ..pydantic import Version


class PaletteEntry(BaseModel):
    name: str
    description: Optional[str] = None
    color: Color


# Dublin Core Metadata https://www.dublincore.org/specifications/dublin-core/dcmi-terms/#section-3
# "title" = Gonzago Framework Editor Icon
# "description" = A skull with a crown in reference to The Murder of Gonzago
# "identifier" = gonzago.palettes.name
# "subject" = palette, gonzago
# "date" = 2023-11-19
# "source" = https://github.com/godot-gonzago
# "relation" = http://asdffasd same as source before
# "language" = en
# "creator" = David Krummenacher
# "contributor" = David Krummenacher, David Krummenacher
# "publisher" = Gonzago Framework
# "rights" = Copyright (c) 2023 David Krummenacher and Gonzago Framework contributors
# "coverage" = ???
# "license" = http://creativecommons.org/licenses/by/4.0/


class Palette(BaseModel):
    name: str
    description: Optional[str] = None
    version: Optional[Version] = None
    author: Optional[str] = None
    source: Optional[str] = None
    colors: List[PaletteEntry]
