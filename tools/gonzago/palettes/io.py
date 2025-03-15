# https://play.pixelblaster.ro/blog/2017/12/18/a-quick-and-dirty-mini-plugin-system-for-python/
# https://kaleidoescape.github.io/decorated-plugins/
import os
from pathlib import Path
from typing import (
    Any,
    Callable,
    Dict,
    Iterator,
    NamedTuple,
    Optional,
    Protocol,
    runtime_checkable,
)

#from ..exceptions import FileTypeError, NameConflictError
from ..io import gather_files
from .core import Palette, Reader, Writer, get_reader_for_file, get_readers, get_writer_from_id


def read(file: Path) -> Palette:
    if not file.exists():
        raise FileNotFoundError(file)
    reader: Reader = get_reader_for_file(file)
    palette: Palette = reader.read(file)
    return palette
    #raise ValueError(f"File at path {file} cannot be read.")


def get_writer_path(id: str, file: Path) -> Path:
    if not file.suffix:
        raise ValueError(f"File path {file} is missing a suffix.")
    writer: Writer = get_writer_from_id(id)
    return file.with_suffix(writer.suffix)


#def write(file: Path, palette: Palette) -> None:
#    if not file.suffix:
#        raise ValueError(f"File path {file} is missing a suffix.")
#    for _, writer in WRITERS.items():
#        if file.suffix == writer.suffix:  # Here lies the problem with scaled png
#            file.parent.mkdir(parents=True, exist_ok=True)  # Ensure folders
#            writer.write(palette, file)
#            return
#    raise ValueError(f"File at path {file} cannot be written.")


def _match_reader(file: Path) -> bool:
    for reader in get_readers():
        if file.match(reader.pattern):
            return True
    return False


def find_palettes(root: Path, max_depth: int = -1) -> Iterator[Path]:
    return gather_files(root, _match_reader, max_depth=max_depth)


# def find_valid_palettes(root: Path, max_depth: int = -1) -> Iterator[Palette]:
#    for file in find_palettes(root):
#        try:
#            palette: Palette = read(file)
#            yield palette
#        except Exception as e:
#            continue


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
                yield ValidationResult(file, reader, ValueError(f"File at path {file} cannot be read by reader with id {reader.id}."))
            continue
        try:
            palette: Palette = reader.read(file)
            del palette
            yield ValidationResult(file, reader)
        except Exception as e:
            yield ValidationResult(file, reader, e)
    yield ValidationResult(file, exception=ValueError(f"File at path {file} is invalid."))
