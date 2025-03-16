from __future__ import annotations

from abc import ABC, abstractmethod
from importlib import import_module
from pathlib import Path
from typing import Annotated, ClassVar, Iterator, List, Optional

from pydantic import BaseModel, ConfigDict, StringConstraints

from ..models import Palette


class PaletteReader(BaseModel, ABC):
    model_config = ConfigDict(frozen=True)

    _READERS: ClassVar[List[PaletteReader]] = []

    id: Annotated[str, StringConstraints(min_length=1)]
    description: Annotated[Optional[str], StringConstraints(min_length=1)]
    pattern: Annotated[
        str, StringConstraints(pattern=r"^(?:/?\*{0,2}\.?[a-zA-Z][a-zA-Z0-9]*)+$")
    ]
    internal: bool = False

    @abstractmethod
    def read(self, file: Path) -> Palette:
        pass

    @abstractmethod
    def validate(self, file: Path) -> bool:
        pass

    @classmethod
    def _register_reader(cls, instance: PaletteReader) -> None:
        if any(e.id == instance.id for e in cls._READERS):
            raise ValueError(
                f"Reader with id {instance.id} already present. All Readers must have unique ids."
            )
        cls._READERS.append(instance)

    @classmethod
    def get_readers(
        cls, external: bool = True, internal: bool = False
    ) -> Iterator[PaletteReader]:
        for reader in cls._READERS:
            if (not reader.internal and external) or (reader.internal and internal):
                yield reader

    @classmethod
    def get_reader_from_id(cls, id: str) -> PaletteReader:
        for reader in cls._READERS:
            if reader.id == id:
                return reader
        raise ValueError(f"There is no reader with id {id}.")

    @classmethod
    def get_reader_for_file(cls, file: Path) -> PaletteReader:
        if not file.is_file():
            raise ValueError(f"Path {file} is not a file.")
        if not file.suffix:
            raise ValueError(f"File path {file} is missing a suffix.")
        if not file.exists(follow_symlinks=True):
            raise FileNotFoundError(f"File at path {file} does not exist.")

        for reader in cls._READERS:
            if file.match(reader.pattern):
                return reader

        raise ValueError(f"No reader found for path {file}.")


class PaletteWriter(BaseModel, ABC):
    model_config = ConfigDict(frozen=True)

    _WRITERS: ClassVar[List[PaletteWriter]] = []

    id: Annotated[str, StringConstraints(min_length=1)]
    description: Annotated[Optional[str], StringConstraints(min_length=1)]
    suffix: Annotated[str, StringConstraints(pattern=r"^(?:\.[a-zA-Z][a-zA-Z0-9]*)+$")]
    internal: bool = False

    @abstractmethod
    def write(self, palette: Palette, file: Path) -> None:
        pass

    @classmethod
    def _register_writer(cls, instance: PaletteWriter) -> None:
        if any(e.id == instance.id for e in cls._WRITERS):
            raise ValueError(
                f"Writer with id {instance.id} already present. All Writers must have unique ids."
            )
        cls._WRITERS.append(instance)

    @classmethod
    def get_writers(
        cls, external: bool = True, internal: bool = False
    ) -> Iterator[PaletteWriter]:
        for writer in cls._WRITERS:
            if (not writer.internal and external) or (writer.internal and internal):
                yield writer

    @classmethod
    def get_writer_from_id(cls, id: str) -> PaletteWriter:
        for writer in cls._WRITERS:
            if writer.id == id:
                return writer
        raise ValueError(f"There is no writer with id {id}.")

    @classmethod
    def get_writers_for_file(cls, file: Path) -> Iterator[PaletteWriter]:
        if not file.is_file():
            raise ValueError(f"Path {file} is not a file.")
        if not file.suffix:
            raise ValueError(f"File path {file} is missing a suffix.")

        posix: str = file.as_posix()
        for writer in cls._WRITERS:
            if posix.endswith(writer.suffix):
                yield writer

        raise ValueError(f"No reader found for path {file}.")


__all__ = ["PaletteReader", "PaletteWriter"]


# Import all modules
for f in Path(__file__).parent.glob("*.py"):
    module_name = f.stem
    if (not module_name.startswith("_")) and (module_name not in globals()):
        import_module(f".{module_name}", __package__)
    del f, module_name
