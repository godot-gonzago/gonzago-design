import os
import yaml
import hashlib
from pathlib import Path
from utils import paths

def compute_md5(path: str | os.PathLike) -> str:
    path = Path(path)

    if path.is_dir():
        return hashlib.md5(path).hexdigest()

    if path.is_file():
        md5 = hashlib.md5()
        with path.open('rb') as file:
            while chunk := file.read(65536): # 64kb chunks
                md5.update(chunk)
        return md5.hexdigest()

    return ""


def load_cache_from_file():
    if not paths.FILE_CACHE.exists():
        return {}
    with paths.FILE_CACHE.open() as file:
        return yaml.full_load(file)


def save_cache_to_file(cache):
    paths.create_directories(paths.CACHE_DIR)
    with paths.FILE_CACHE.open('w+') as file:
        yaml.dump(cache, file)


def gather_file_cache():
    cache = {}
    for (root, dirs, files) in os.walk(paths.SOURCE_DIR):
        for file in files:
            #file.endswith()
            file_path = paths.SOURCE_DIR.joinpath(root, file)
            #print(f'Suffix: {file_path.suffix}')
            rel_path = file_path.relative_to(paths.SOURCE_DIR).as_posix()

            statinfo = os.stat(file_path)
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
