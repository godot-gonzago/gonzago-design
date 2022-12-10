from os import PathLike
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent.parent
SOURCE_DIR = ROOT_DIR.joinpath('source')
EXPORT_DIR = ROOT_DIR

CACHE_DIR = ROOT_DIR.joinpath('.cache')
FILE_CACHE = CACHE_DIR.joinpath('files.yaml')


def create_directories(path: str | PathLike):
    path = Path(path)
    if path.is_file():
        path = path.parent
    if not path.exists():
        path.mkdir(parents=True, exist_ok=True)
