from datetime import date as Date
from enum import Enum
import getpass
from pathlib import Path
from typing import Annotated, Callable, Dict, Iterator, List, NamedTuple, Optional

from pydantic import BaseModel, Field, StringConstraints
from pydantic_extra_types.color import Color
from pydantic_extra_types.semantic_version import SemanticVersion as Version
from pydantic_extra_types.language_code import LanguageAlpha2


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
    colors: Annotated[List[PaletteEntry], Field(min_length=1)]
    mapped_title: Annotated[Optional[str], StringConstraints(min_length=1)] = None
    mapped_description: Annotated[Optional[str], StringConstraints(min_length=1)] = None
    mapped_suffix: Annotated[
        Optional[str],
        StringConstraints(
            min_length=1, pattern=r"^[a-z]+(?:\_[a-z]+)*(?:\.[a-z]+(?:\_[a-z]+)*)*$"
        ),
    ] = None


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

    black: PaletteEntry = PaletteEntry.model_construct()
    black.name = "Black"
    black.color = Color("black")

    white: PaletteEntry = PaletteEntry.model_construct()
    black.name = "White"
    black.color = Color("white")

    palette: Palette = PaletteEntry.model_construct()
    palette.title = title
    palette.colors = [black, white]

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


Read = Callable[[Path], Palette]
Validate = Callable[[Path], bool]


class Reader(NamedTuple):
    id: str
    pattern: str
    description: str
    read: Read
    validate: Validate
    internal: bool = False


_READERS: Dict[str, Reader] = dict[str, Reader]()


def register_reader(
    id: str, pattern: str, description: str, read: Read, validate: Validate, internal: bool = False
) -> None:
    if id in _READERS:
        raise ValueError(
            f"Reader with id {id} already present. All Readers must have unique ids."
        )
    _READERS[id] = Reader(id, pattern, description, read, validate, internal)


def get_readers(external: bool = True, internal: bool = False) -> Iterator[Reader]:
    for _, reader in _READERS.items():
        if (not reader.internal and external) or (reader.internal and internal):
            yield reader


def get_reader_from_id(id: str) -> Reader:
    if id in _READERS.keys():
        return _READERS[id]
    raise ValueError(f"There is no reader with id {id}.")


def get_reader_for_file(file: Path) -> Reader:
    if not file.is_file():
        raise ValueError(f"Path {file} is not a file.")
    if not file.suffix:
        raise ValueError(f"File path {file} is missing a suffix.")
    if not file.exists(follow_symlinks=True):
        raise FileNotFoundError(f"File at path {file} does not exist.")

    for _, reader in _READERS.items():
        if file.match(reader.pattern):
            return reader

    raise ValueError(f"No reader found for path {file}.")


Write = Callable[[Palette, Path], None]


class Writer(NamedTuple):
    id: str
    suffix: str
    description: str
    write: Write
    internal: bool = False

    def build_file_path(self, file: Path) -> Path:
        if not file.suffix:
            raise ValueError(f"File path {file} is missing a suffix.")
        return file.with_suffix(self.suffix)


_WRITERS: Dict[str, Writer] = dict[str, Writer]()


def register_writer(
    id: str,
    suffix: str,
    description: str,
    write: Write,
    internal: bool = False,
) -> None:
    if id in _WRITERS:
        raise ValueError(
            f"Writer with id {id} already present. All Writers must have unique ids."
        )
    _WRITERS[id] = Writer(
        id,
        suffix,
        description,
        write,
        internal,
    )


def get_writers(external: bool = True, internal: bool = False) -> Iterator[Writer]:
    for _, writer in _WRITERS.items():
        if (not writer.internal and external) or (writer.internal and internal):
            yield writer


def get_writer_from_id(id: str) -> Writer:
    if id in _WRITERS.keys():
        return _WRITERS[id]
    raise ValueError(f"There is no writer with id {id}.")


#class PaletteFile(NamedTuple):
#    path: Path
#    rel_path: Path
#
#    def read(file: Path) -> Palette:
#        if not file.exists():
#            raise FileNotFoundError(f"File not found at path {file}.")
#        reader: Reader = get_reader_for_file(file)
#        palette: Palette = reader.read(file)
#        return palette
#
#    def write(writer: Writer, palette: Palette, file: Path) -> None:
#        if not file.suffix:
#            raise ValueError(
#                f"File path {file} has wrong suffix. Writer needs suffix {writer.suffix}."
#            )
#        writer.write(palette, file)
