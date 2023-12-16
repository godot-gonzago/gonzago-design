# https://play.pixelblaster.ro/blog/2017/12/18/a-quick-and-dirty-mini-plugin-system-for-python/
# https://kaleidoescape.github.io/decorated-plugins/
import os
from pathlib import Path
from typing import Callable, Iterator, List, NamedTuple, Optional

from pydantic import BaseModel
from pydantic_extra_types.color import Color
from ..pydantic import Version


class NameConflictError(ValueError):
    pass


# raise when file cannot be read.
class FileTypeError(TypeError):
    pass


class PaletteEntry(BaseModel):
    name: str
    description: Optional[str] = None
    color: Color


class Palette(BaseModel):
    name: str
    description: Optional[str] = None
    version: Optional[Version] = None
    author: Optional[str] = None
    source: Optional[str] = None
    colors: List[PaletteEntry]


Read = Callable[[Path], Palette]


class Reader(NamedTuple):
    id: str
    pattern: str
    description: str
    read: Read


READERS = dict[str, Reader]()


def register_reader(
    id: str,
    pattern: str,
    description: str,
    read: Read,
) -> None:
    if id in READERS:
        raise NameConflictError(
            f"Reader with id {id} already present. All Readers must have unique ids."
        )
    READERS[id] = Reader(id, pattern, description, read)


def get_readers() -> Iterator[Reader]:
    for _, reader in READERS.items():
        yield reader


def read(file: Path) -> Palette:
    if not file.exists():
        raise FileNotFoundError(file)
    for _, reader in READERS.items():
        if not file.match(reader.pattern):
            continue
        try:
            palette: Palette = reader.read(file)
            return palette
        except Exception as e:
            continue
    raise FileTypeError(file)


def _match_reader(file: Path) -> bool:
    for _, reader in READERS.items():
        if file.match(reader.pattern):
            return True
    return False


# TODO: For check function create validation function that returns validation results.
#       Contains references to file path, possible readers (based on pattern match)
#       and possible exceptions. No exceptions means validation passed.

class ValidationResult(NamedTuple):
    file: Path
    reader: Optional[Reader] = None
    exception: Optional[Exception] = None


def validate(file: Path, include_mismatch: bool = False) -> Iterator[ValidationResult]:
    # TODO: return correct errors!
    if not file.exists():
        yield ValidationResult(file, exception=FileNotFoundError(file))
        raise StopIteration
    for _, reader in READERS.items():
        if not file.match(reader.pattern):
            if include_mismatch:
                yield ValidationResult(file, reader, FileTypeError(file))
            continue
        try:
            palette: Palette = reader.read(file)
            del palette
            yield ValidationResult(file, reader)
        except Exception as e:
            yield ValidationResult(file, reader, e)
    yield ValidationResult(file, exception=FileTypeError(file))


Write = Callable[[str, Path, Palette], None]


class Writer(NamedTuple):
    id: str
    suffix: str
    description: str
    write: Write
    default: bool = True


WRITERS = dict[str, Writer]()


def register_writer(
    id: str,
    suffix: str,
    description: str,
    write: Write,
    default: bool = True,
) -> None:
    if id in WRITERS:
        raise NameConflictError(
            f"Writer with id {id} already present. All Writers must have unique ids."
        )
    WRITERS[id] = Writer(
        id,
        suffix,
        description,
        write,
        default,
    )


def get_writers(include_default: bool = False) -> Iterator[Writer]:
    for _, writer in WRITERS.items():
        if writer.default or include_default:
            yield writer


def write(id: str, file: Path, palette: Palette) -> None:
    if not file.is_file():
        raise FileTypeError(file)
    for _, writer in WRITERS.items():
        if not writer.default:
            continue
        try:
            writer.write(id, file, palette)
            return
        except Exception as e:
            continue
    raise FileTypeError(file)


def find_palettes(root: Path) -> Iterator[Path]:
    root = root.resolve()
    if not root.exists():
        raise FileNotFoundError(f"{root} does not exist")

    if root.is_file():
        # if root.match(TEMPLATE_FILE_PATTERN):
        #    yield root
        # raise TypeError(f"{root} is not a valid template path")
        yield root

    for current, dirs, files in os.walk(root):
        for name in dirs:
            if name.startswith("_"):
                dirs.remove(name)
        for name in files:
            if _match_reader(Path(name)):
                path: Path = root.joinpath(current, name)
                yield path
