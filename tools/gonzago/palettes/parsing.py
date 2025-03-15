from pathlib import Path
from typing import Callable, Dict, Iterator, NamedTuple

from .models import Palette


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


#def get_reader_for_file(file: Path) -> Reader:
#    if not file.is_file():
#        raise ValueError(f"Path {file} is not a file.")
#    if not file.suffix:
#        raise ValueError(f"File path {file} is missing a suffix.")
#    if not file.exists(follow_symlinks=True):
#        raise FileNotFoundError(f"File at path {file} does not exist.")
#
#    for _, reader in _READERS.items():
#        if file.match(reader.pattern):
#            return reader
#
#    raise ValueError(f"No reader found for path {file}.")


Write = Callable[[Palette, Path], None]


class Writer(NamedTuple):
    id: str
    suffix: str
    description: str
    write: Write
    internal: bool = False


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


#def get_writers_for_file(file: Path) -> Iterator[Writer]:
#    if not file.is_file():
#        raise ValueError(f"Path {file} is not a file.")
#    if not file.suffix:
#        raise ValueError(f"File path {file} is missing a suffix.")
#
#    posix: str = file.as_posix()
#    for _, writer in _WRITERS.items():
#        if posix.endswith(writer.suffix):
#            yield writer
#
#    raise ValueError(f"No reader found for path {file}.")
