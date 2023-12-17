import os
from pathlib import Path
from typing import Callable, Iterator, Optional


# _PathMatch = [Callable[[Path], bool] | str | None]
PathMatch = Optional[Callable[[Path], bool]]


def default_dir_match(path: Path) -> bool:
    return path.match("[!._]*")


def gather_files(
    root: Path,
    file_match: PathMatch = None,
    dir_match: PathMatch = default_dir_match,
    max_depth: int = -1,
) -> Iterator[Path]:
    root = root.resolve()
    if not root.exists():
        raise FileNotFoundError(root)

    if root.is_file():
        if file_match and not file_match(root):
            raise TypeError(root)
        else:
            yield root
        raise StopIteration

    depth_check: bool = max_depth > -1
    depth: int = 0

    for current, dirs, files in os.walk(root):
        if depth_check and depth >= max_depth:
            dirs.clear()
        depth += 1

        if dir_match != None:
            for name in dirs:
                path: Path = root.joinpath(current, name)
                # if (
                #     dir_match is str and not path.match(dir_match)
                #     or not dir_match(path)
                # ):
                #     dirs.remove(name)
                if not dir_match(path):
                    dirs.remove(name)

        for name in files:
            path: Path = root.joinpath(current, name)
            if file_match and not file_match(path):
                continue
            yield path
