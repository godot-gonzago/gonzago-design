from datetime import date as Date
from enum import Enum
from typing import Annotated, List, Optional

from pydantic import BaseModel, Field, HttpUrl, StringConstraints
from pydantic_extra_types.language_code import LanguageAlpha2
from pydantic_extra_types.semantic_version import SemanticVersion as Version


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
    license: Optional[HttpUrl] = None
    coverage: Optional[str] = None
    # format: Optional[str] = None # mime type
    # type: Optional[str] = None
    # subject: Optional[str] = None
    # keywords: Optional[List[str]] = None # instead of subject list
