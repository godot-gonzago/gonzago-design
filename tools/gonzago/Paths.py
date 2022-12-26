from os import PathLike
from pathlib import PurePath, Path

_SCRIPT_FILE: PurePath = PurePath(__file__)
_SCRIPT_DIR: PurePath = _SCRIPT_FILE.parent
_TOOLS_DIR: PurePath = _SCRIPT_DIR.parent

CONFIG_DIR: PurePath = _TOOLS_DIR.joinpath('config')
CACHE_DIR: PurePath = _TOOLS_DIR.joinpath('.cache')
TEMP_DIR: PurePath = _TOOLS_DIR.joinpath('.temp')

ROOT_DIR: PurePath = _TOOLS_DIR.parent
SOURCE_DIR: PurePath = ROOT_DIR.joinpath('source')
EXPORT_DIR: PurePath = ROOT_DIR

StrPath: type = str | PathLike


def get_pure_path(path: StrPath) -> PurePath:
    if path is PurePath:
        return path
    return PurePath(path)


def get_path(path: StrPath) -> Path:
    if path is Path:
        return path
    return Path(path)
