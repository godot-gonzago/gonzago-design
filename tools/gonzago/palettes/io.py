# https://play.pixelblaster.ro/blog/2017/12/18/a-quick-and-dirty-mini-plugin-system-for-python/
# https://kaleidoescape.github.io/decorated-plugins/
from pathlib import Path
from typing import (
    Iterator,
    NamedTuple,
    Optional,
)

from ..io import gather_files
from .parsing import Reader, get_readers


class PaletteFile(NamedTuple):
    path: Path
    rel_path: Optional[Path] = None
    reader: Optional[Reader] = None


def get_palette_files(root: Path, max_depth: int = -1) -> Iterator[PaletteFile]:
    for file in gather_files(root, max_depth=max_depth):
        for reader in get_readers(internal=True):
            if file.match(reader.pattern):
                rel_path: Path = file.relative_to(root)
                yield PaletteFile(file, rel_path, reader)
