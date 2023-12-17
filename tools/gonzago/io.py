import os
from pathlib import Path
from typing import Iterator, Optional, Protocol, runtime_checkable


@runtime_checkable
class _PathMatcher(Protocol):
    def __call__(self, path: Path) -> bool:
        ...

_PathFilter = Optional[_PathMatcher | str]


def filter_path(path: Path, filter: _PathFilter) -> bool:
    match filter:
        case None:
            return True
        case str():
            return path.match(filter)
        case _PathMatcher():
            return filter(path)
        case _:
            return True


def gather_files(
    root: Path,
    file_filter: _PathFilter = None,
    dir_filter: _PathFilter = "[!._]*",
    max_depth: int = -1,
) -> Iterator[Path]:
    root = root.resolve()
    if not root.exists():
        raise FileNotFoundError(root)

    if root.is_file():
        if not filter_path(root, file_filter):
            raise TypeError(root)
        yield root
        return

    depth_check: bool = max_depth > -1
    depth: int = 0

    for current, dirs, files in os.walk(root):
        if depth_check and depth >= max_depth:
            dirs.clear()
        depth += 1

        if not dir_filter is None:
            for name in dirs:
                path: Path = root.joinpath(current, name)
                if not filter_path(path, dir_filter):
                    dirs.remove(name)

        for name in files:
            path: Path = root.joinpath(current, name)
            if filter_path(path, file_filter):
                yield path
