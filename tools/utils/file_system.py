import hashlib
from os import PathLike, walk, stat
from pathlib import Path

import yaml

_SCRIPT_FILE = Path(__file__)
_SCRIPT_DIR = _SCRIPT_FILE.parent
_TOOLS_DIR = _SCRIPT_DIR.parent

_CACHE_DIR = _TOOLS_DIR.joinpath('.cache')
_CACHE_FILE = _CACHE_DIR.joinpath('files.yaml')

ROOT_DIR = _TOOLS_DIR.parent
SOURCE_DIR = ROOT_DIR.joinpath('source')
EXPORT_DIR = ROOT_DIR


def create_directories(path: str | PathLike) -> None:
    if not path is Path:
        path = Path(path)

    if not path.is_dir():
        path.mkdir(parents=True, exist_ok=True)


def compute_md5(path: str | PathLike) -> str:
    if not path is Path:
        path = Path(path)

    if path.is_dir():
        return hashlib.md5(path).hexdigest()

    if path.is_file():
        md5 = hashlib.md5()
        with path.open('rb') as file:
            while chunk := file.read(65536):  # 64kb chunks
                md5.update(chunk)
        return md5.hexdigest()

    return ""


def load_cache_from_file() -> dict:
    if not _CACHE_FILE.exists():
        return {}

    with _CACHE_FILE.open() as file:
        return yaml.full_load(file)


def save_cache_to_file(cache: dict) -> None:
    create_directories(_CACHE_DIR)
    with _CACHE_FILE.open('w+') as file:
        yaml.dump(cache, file)


def gather_file_cache():
    cache = {}
    for (root, dirs, files) in walk(SOURCE_DIR):
        for file in files:
            # file.endswith()
            file_path = SOURCE_DIR.joinpath(root, file)
            # print(f'Suffix: {file_path.suffix}')
            rel_path = file_path.relative_to(SOURCE_DIR).as_posix()

            statinfo = stat(file_path)
            cache[rel_path] = {
                'lmod': statinfo.st_mtime,
                'size': statinfo.st_size,
                'hash': compute_md5(file_path)
            }

    return cache


def diff_file_cache():
    old_cache = load_cache_from_file()
    current_cache = gather_file_cache()

    new = []
    changed = []
    deleted = list(old_cache.keys())

    for rel_path in current_cache:
        if not rel_path in old_cache:
            new.append(rel_path)
            continue

        # TODO: Handle removed files?
        deleted.remove(rel_path)

        old_file_info = old_cache[rel_path]
        current_file_info = current_cache[rel_path]

        # TODO: this can be integratet into the gathering process for optimization because me might don't
        # need to calculate md5 hash!
        if old_file_info['lmod'] == current_file_info['lmod']:
            continue
        if old_file_info['hash'] == current_file_info['hash']:
            continue
        changed.append(rel_path)

    print('New files:')
    print(new)
    print('Changed files:')
    print(changed)
    print('Deleted files:')
    print(deleted)

    save_cache_to_file(current_cache)


if __name__ == '__main__':
    print('Gathering files')
    print('===============')

    diff_file_cache()
