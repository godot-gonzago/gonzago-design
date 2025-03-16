import os
from pathlib import Path
from typing import Callable, Iterator, Optional

PathMatcher = Callable[[Path], bool]
PathFilter = Optional[PathMatcher | str]


def filter_path(path: Path, filter: PathFilter) -> bool:
    match filter:
        case None:
            return True
        case str():
            return path.match(filter)
        case fn if PathMatcher:
            return fn(path)
        case _:
            return True


def gather_files(
    root: Path,
    file_filter: PathFilter = None,
    dir_filter: PathFilter = "[!._]*",
    max_depth: int = -1,
) -> Iterator[Path]:
    root = root.resolve()
    if not root.exists():
        raise FileNotFoundError(
            f"File does not exist at {root}."
            if root.is_file()
            else f"Directory does not exist at {root}."
        )

    if root.is_file():
        if not filter_path(root, file_filter):
            raise TypeError(f"File at path {root} failes filter.")
        yield root
        return

    depth_check: bool = max_depth > -1
    depth: int = 0

    for current, dirs, files in os.walk(root):
        if depth_check and depth >= max_depth:
            dirs.clear()
        depth += 1

        if dir_filter is not None:
            for name in dirs:
                path: Path = root.joinpath(current, name)
                if not filter_path(path, dir_filter):
                    dirs.remove(name)

        for name in files:
            path: Path = root.joinpath(current, name)
            if filter_path(path, file_filter):
                yield path


def ensure_folders(absolute_path: Path) -> None:
    if not absolute_path.is_absolute():
        raise ValueError(
            f"Cannot ensure folders along path {absolute_path} as it is not absolute."
        )
    if absolute_path.is_file():
        absolute_path = absolute_path.parent
    absolute_path.parent.mkdir(parents=True, exist_ok=True)  # Ensure folders
