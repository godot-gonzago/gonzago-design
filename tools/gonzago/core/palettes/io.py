# https://play.pixelblaster.ro/blog/2017/12/18/a-quick-and-dirty-mini-plugin-system-for-python/
# https://kaleidoescape.github.io/decorated-plugins/
from pathlib import Path
from typing import Iterator, Optional

from pydantic import BaseModel

from ..io import gather_files
from .models import Palette
from .parsing import PaletteReader, PaletteWriter


class PaletteFile(BaseModel):
    path: Path
    rel_path: Path
    palette: Optional[Palette] = None

    def as_posix(self) -> str:
        return self.rel_path.as_posix()


class WritablePaletteFile(PaletteFile):
    writer: PaletteWriter

    def write(self) -> None:
        if not self.writer:
            raise ValueError(f"Writer is null for Palette with path {self.path}.")
        self.writer.write(self.palette, self.path)


class ReadablePaletteFile(PaletteFile):
    reader: PaletteReader

    def read(self) -> Palette:
        if not self.reader:
            raise ValueError(f"Reader is null for Palette with path {self.path}.")
        if not self.palette:
            self.palette = self.reader.read(self.path)
        return self.palette

    def create_output_file(
        self, dir: Path, writer: PaletteWriter
    ) -> WritablePaletteFile:
        # if not file.suffix:
        #    raise ValueError(f"File path {file} is missing a suffix.")
        rel_path: Path = self.rel_path.with_suffix(writer.suffix)
        path: Path = dir.joinpath(rel_path).resolve()
        palette: Palette = self.read()
        return WritablePaletteFile(
            path=path, rel_path=rel_path, writer=writer, palette=palette
        )


def get_palette_file(file: Path) -> ReadablePaletteFile:
    for reader in PaletteReader.get_readers(internal=True):
        if file.match(reader.pattern):
            rel_path: Path = file.relative_to(file.parent)
            return ReadablePaletteFile(path=file, rel_path=rel_path, reader=reader)


def get_palette_files(root: Path, max_depth: int = -1) -> Iterator[ReadablePaletteFile]:
    for file in gather_files(root, max_depth=max_depth):
        for reader in PaletteReader.get_readers(internal=True):
            if file.match(reader.pattern):
                rel_path: Path = file.relative_to(root)
                yield ReadablePaletteFile(path=file, rel_path=rel_path, reader=reader)
