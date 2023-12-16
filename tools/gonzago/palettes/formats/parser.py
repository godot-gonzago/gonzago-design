# https://play.pixelblaster.ro/blog/2017/12/18/a-quick-and-dirty-mini-plugin-system-for-python/
# https://kaleidoescape.github.io/decorated-plugins/
from pathlib import Path
from typing import Callable, Iterator, NamedTuple, Protocol

from ..templates import Template


class NameConflictError(ValueError):
    pass


# raise when file cannot be read.
class FileTypeError(TypeError):
    pass


Read = Callable[[Path], Template]
Write = Callable[[str, Path, Template], None]


class Reader(NamedTuple):
    id: str
    pattern: str
    description: str
    read: Read
    default: bool = True


READERS = dict[str, Reader]()


def register_reader(
    id: str,
    pattern: str,
    description: str,
    read: Read,
    default: bool = True,
) -> None:
    if id in READERS:
        raise NameConflictError(
            f"Reader with id {id} already present. All Readers must have unique ids."
        )
    READERS[id] = Reader(id, pattern, description, read, default)


def get_readers() -> Iterator[Reader]:
    for _, reader in READERS.items():
        yield reader


def read(file: Path) -> Template:
    if not file.exists():
        raise FileNotFoundError(file)
    for _, reader in READERS.items():
        if not reader.default or not file.match(reader.pattern):
            continue
        try:
            template: Template = reader.read(file)
            return template
        except Exception as e:
            continue
    raise FileTypeError(file)


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


def get_writers() -> Iterator[Writer]:
    for _, writer in WRITERS.items():
        yield writer


def write(id: str, file: Path, template: Template) -> None:
    if not file.is_file():
        raise FileTypeError(file)
    for _, writer in WRITERS.items():
        if not writer.default:
            continue
        try:
            writer.write(id, file, template)
            return
        except Exception as e:
            continue
    raise FileTypeError(file)
