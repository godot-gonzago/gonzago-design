from datetime import date as Date
from pathlib import Path
from typing import Annotated, List, Optional
from pydantic import BaseModel, PositiveInt, constr, FilePath, StringConstraints

from ..pydantic import Version


class ViewBox(BaseModel):
    x: int = 0
    y: int = 0
    width: PositiveInt = 0
    height: PositiveInt = 0


class SVGMetaData(BaseModel):
    width: Optional[PositiveInt ] = None
    height: Optional[PositiveInt ] = None
    view_box: Optional[ViewBox] = None
    title: Optional[str] = None
    description: Optional[str] = None
    version: Optional[Version] = None
    date: Optional[Date] = None
    language: Optional[str] = None
    identifier: Optional[str] = None
    subject: Optional[List[str]] = None
    relation: Optional[str] = None
    source: Optional[str] = None
    publisher: Optional[str] = None
    creator: Optional[str] = None
    contributor: Optional[List[str]] = None
    rights: Optional[str] = None
    license: Optional[str] = None
    coverage: Optional[str] = None


class SVGFile(BaseModel):
    path: FilePath
    meta: SVGMetaData = SVGMetaData()
