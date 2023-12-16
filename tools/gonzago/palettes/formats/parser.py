# https://play.pixelblaster.ro/blog/2017/12/18/a-quick-and-dirty-mini-plugin-system-for-python/
# https://kaleidoescape.github.io/decorated-plugins/
from pathlib import Path
from typing import Callable, NamedTuple, Protocol

from gonzago.palettes.templates import Template


class NameConflictError(ValueError):
    pass


CanHandleId = Callable[[str], bool]

CanRead = Callable[[Path], bool]
Read = Callable[[Path], Template]

ChangePathFromId = Callable[[str, Path], Path]
CanWrite = Callable[[Path], bool]
Write = Callable[[Path, Template], None]


class Reader(NamedTuple):
    id: str
    suffix: str
    description: str
    can_handle_id: CanHandleId
    can_read: CanRead
    read: Read
    default: bool = True


READERS = dict[str, Reader]()


def register_reader(
    id: str,
    suffix: str,
    description: str,
    can_handle_id: CanHandleId,
    can_read: CanRead,
    read: Read,
    default: bool = True,
) -> None:
    if id in READERS:
        raise NameConflictError(
            f"Reader with id {id} already present. All Readers must have unique ids."
        )
    READERS[id] = Reader(
        id, suffix, description, can_handle_id, can_read, read, default
    )


class Writer(NamedTuple):
    id: str
    suffix: str
    description: str
    can_handle_id: CanHandleId
    change_path_from_id: ChangePathFromId
    can_write: CanWrite
    write: Write
    default: bool = True


WRITERS = dict[str, Writer]()


def register_writer(
    id: str,
    suffix: str,
    description: str,
    can_handle_id: CanHandleId,
    change_path_from_id: ChangePathFromId,
    can_write: CanWrite,
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
        can_handle_id,
        change_path_from_id,
        can_write,
        write,
        default,
    )
