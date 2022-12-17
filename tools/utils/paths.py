from os import PathLike
from pathlib import Path

_SCRIPT_FILE = Path(__file__)
_SCRIPT_DIR = _SCRIPT_FILE.parent

TOOLS_DIR = _SCRIPT_DIR.parent.parent
CACHE_DIR = TOOLS_DIR.joinpath('.cache')

ROOT_DIR = TOOLS_DIR.parent
SOURCE_DIR = ROOT_DIR.joinpath('source')
EXPORT_DIR = ROOT_DIR


def create_directories(path: str | PathLike):
    if not path is Path:
        path = Path(path)
    if path.is_file():
        path = path.parent
    if not path.exists():
        path.mkdir(parents=True, exist_ok=True)
