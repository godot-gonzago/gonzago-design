import os
from pathlib import Path
from typing import Callable, Iterator


PathMatcher = Callable[[Path], bool]
PathSelector = [PathMatcher | str | None]


def check_path_selector(selector: PathSelector, path: Path) -> bool:
    match selector:
        case None:
            return True
        case str():
            return path.match(selector)
        case _:
            if selector is PathMatcher:
                return selector(path)
            return True


def gather_files(
    root: Path,
    file_match: PathSelector = None,
    dir_match: PathSelector = "[!._]*",
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
                if not check_path_selector(dir_match, path):
                    dirs.remove(name)

        for name in files:
            path: Path = root.joinpath(current, name)
            if not check_path_selector(file_match, path):
                continue
            yield path
