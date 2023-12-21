# https://play.pixelblaster.ro/blog/2017/12/18/a-quick-and-dirty-mini-plugin-system-for-python/
# https://kaleidoescape.github.io/decorated-plugins/
import os
from pathlib import Path
from typing import (
    Any,
    Callable,
    Iterator,
    NamedTuple,
    Optional,
    Protocol,
    runtime_checkable,
)

from ..io import gather_files
from .core import Palette
from .exceptions import FileTypeError, NameConflictError


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
        if file.match(reader.pattern):
            palette: Palette = reader.read(file)
            return palette
    raise FileTypeError(file)


Write = Callable[[Palette, Path], None]


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


def get_writers(include_non_default: bool = False) -> Iterator[Writer]:
    for _, writer in WRITERS.items():
        if writer.default or include_non_default:
            yield writer


def get_writer_from_id(id: str) -> Writer:
    if id in WRITERS.keys():
        return WRITERS[id]
    raise KeyError()


def get_writer_path(id: str, file: Path) -> Path:
    if not file.suffix:
        raise FileTypeError(file)
    if id in WRITERS.keys():
        return file.with_suffix(WRITERS[id].suffix)
    raise KeyError()


def write(file: Path, palette: Palette) -> None:
    if not file.suffix:
        raise FileTypeError(file)
    for _, writer in WRITERS.items():
        if file.suffix == writer.suffix:  # Here lies the problem with scaled png
            file.parent.mkdir(parents=True, exist_ok=True)  # Ensure folders
            writer.write(palette, file)
            return
    raise FileTypeError(file)


def _match_reader(file: Path) -> bool:
    for _, reader in READERS.items():
        if file.match(reader.pattern):
            return True
    return False


def find_palettes(root: Path, max_depth: int = -1) -> Iterator[Path]:
    return gather_files(root, _match_reader, max_depth=max_depth)


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
