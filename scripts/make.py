import os
import yaml
import hashlib
import pathlib
from pathlib import Path

root_path = Path(__file__).parent.parent
cache_path = root_path.joinpath('.cache/files.yaml')
source_path = root_path.joinpath('source')

# A utility function that can be used in your code
def compute_md5(file_path):
    md5 = hashlib.md5()
    with open(file_path, 'rb') as f:
        while chunk := f.read(65536): # 64kb chunks
            md5.update(chunk)
    return md5.hexdigest()


def load_cache_from_file():
    if not cache_path.exists():
        return {}
    with open(cache_path) as file:
        return yaml.full_load(file)


def save_cache_to_file(cache):
    if not cache_path.parent.exists():
        cache_path.parent.mkdir(parents = True, exist_ok = True)
    with open(cache_path, 'w+') as file:
        yaml.dump(cache, file)

def gather_file_cache():
    cache = {}
    for (root, dirs, files) in os.walk(source_path):
        for file in files:
            #file.endswith()
            file_path = source_path.joinpath(root, file)
            #print(f'Suffix: {file_path.suffix}')
            rel_path = str(file_path.relative_to(source_path))

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
