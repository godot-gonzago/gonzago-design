import hashlib
from os import PathLike, stat, walk
from pathlib import Path

import yaml
import shared.Paths as Paths

_CACHE_FILE: Path = Path(Paths.CACHE_DIR.joinpath('files.yaml'))
_MD5_CHUNK_SIZE: int = 65536  # 64kb chunks


def create_directories(path: Paths.StrPath, is_file_path: bool = False) -> None:
    p: Path = Paths.get_path(path)
    if is_file_path:
        p = p.parent
    if not p.is_dir():
        p.mkdir(parents=True, exist_ok=True)


def compute_md5(path: Paths.StrPath, chunk_size: int = _MD5_CHUNK_SIZE) -> str:
    p: Path = Paths.get_path(path)
    if p.is_dir():
        return hashlib.md5(p.resolve()).hexdigest()
    if p.is_file():
        md5 = hashlib.md5()
        with p.open('rb') as file:
            while chunk := file.read(chunk_size):
                md5.update(chunk)
        return md5.hexdigest()
    return ''


def load_cache_from_file() -> dict:
    if not _CACHE_FILE.exists():
        return {}

    with _CACHE_FILE.open() as file:
        return yaml.full_load(file)


def save_cache_to_file(cache: dict) -> None:
    create_directories(_CACHE_FILE, True)
    with _CACHE_FILE.open('w+') as file:
        yaml.dump(cache, file)


class DirStats:
    lmod: float
    hash: str

    def __init__(self, lmod: float, hash: str):
        self.lmod = lmod
        self.hash = hash

    # https://www.tutorialspoint.com/How-to-overload-Python-comparison-operators


class FileStats:
    lmod: float
    size: int
    hash: str

    def __init__(self, lmod: float, size: int, hash: str):
        self.lmod = lmod
        self.size = size
        self.hash = hash


class FileSystemCache:
    dirs: dict[str, DirStats] = {}
    files: dict[str, FileStats] = {}

    def save(path: str | PathLike = _CACHE_FILE) -> None:
        pass

    def load(path: str | PathLike = _CACHE_FILE) -> None:
        pass

    def gather(self) -> None:
        self.dirs.clear()
        self.files.clear()

        for (root, dirs, files) in walk(Paths.SOURCE_DIR):
            for dir in dirs:
                dir_path: Path = Paths.SOURCE_DIR.joinpath(root, dir)
                rel_path: Path = dir_path.relative_to(
                    Paths.SOURCE_DIR).as_posix()

                statinfo = stat(file_path)
                self.dirs[rel_path] = DirStats(
                    statinfo.st_mtime,
                    statinfo.st_size,
                    compute_md5(dir_path)
                )

            for file in files:
                # file.endswith()
                file_path = Paths.SOURCE_DIR.joinpath(root, file)
                # file_path.match('*.svg')
                # print(f'Suffix: {file_path.suffix}')
                rel_path = file_path.relative_to(Paths.SOURCE_DIR).as_posix()

                statinfo = stat(file_path)
                self.files[rel_path] = FileStats(
                    statinfo.st_mtime,
                    statinfo.st_size,
                    compute_md5(file_path)
                )


# class CacheDiff:
#    new : list[str] = []
#    modified : list[str] = []
#    missing : list[str] = []
#    def __init__():
#        pass


def gather_file_cache() -> dict:
    cache = {}
    for (root, dirs, files) in walk(Paths.SOURCE_DIR):
        for file in files:
            # file.endswith()
            file_path = Paths.SOURCE_DIR.joinpath(root, file)
            # print(f'Suffix: {file_path.suffix}')
            rel_path = file_path.relative_to(Paths.SOURCE_DIR).as_posix()

            statinfo = stat(file_path)
            cache[rel_path] = {
                'lmod': statinfo.st_mtime,
                'size': statinfo.st_size,
                'hash': compute_md5(file_path)
            }

    return cache


def diff_file_cache() -> None:
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
