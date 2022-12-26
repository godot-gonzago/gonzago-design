from os import PathLike
from pathlib import Path, PurePath

_SCRIPT_FILE: PurePath = PurePath(__file__)
_SCRIPT_DIR: PurePath = _SCRIPT_FILE.parent
_TOOLS_DIR: PurePath = _SCRIPT_DIR.parent

CONFIG_DIR: PurePath = _TOOLS_DIR.joinpath('config')
CACHE_DIR: PurePath = _TOOLS_DIR.joinpath('.cache')
TEMP_DIR: PurePath = _TOOLS_DIR.joinpath('.temp')

ROOT_DIR: PurePath = _TOOLS_DIR.parent
SOURCE_DIR: PurePath = ROOT_DIR.joinpath('source')
EXPORT_DIR: PurePath = ROOT_DIR

StrPath = str | PathLike


def get_pure_path(path: StrPath) -> PurePath:
    return path if path is PurePath else PurePath(path)


def get_path(path: StrPath) -> Path:
    return path if path is Path else Path(path)
