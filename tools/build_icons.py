import os
from os import PathLike
from pathlib import Path
from typing import Iterator

from scour import scour

ROOT_DIR = Path(__file__).parent.parent
SOURCE_DIR = ROOT_DIR.joinpath('source', 'icons')
EXPORT_DIR = ROOT_DIR.joinpath('icons')


def ensure_directories(path: str | PathLike) -> None:
    if not path is Path:
        path = Path(path)
    if path.is_file():
        path = path.parent
    if not path.exists():
        path.mkdir(parents=True, exist_ok=True)


def get_source_paths() -> Iterator[Path]:
    for (root, _, files) in os.walk(SOURCE_DIR):
        path = Path(root)
        for file in files:
            if file.endswith('.svg'):
                yield path.joinpath(file)


def get_export_path(source_path: Path) -> Path:
    rel_path = source_path.relative_to(SOURCE_DIR)
    return EXPORT_DIR.joinpath(rel_path)


def build():
    options = scour.parse_args([
        '--set-precision=5',
        '--create-groups',
        '--strip-xml-prolog',
        '--remove-descriptive-elements',
        '--enable-comment-stripping',
        '--enable-viewboxing',
        '--no-line-breaks',
        '--strip-xml-space',
        '--enable-id-stripping',
        '--shorten-ids',
        '--quiet'
    ])

    for source_path in get_source_paths():
        rel_path = source_path.relative_to(SOURCE_DIR).as_posix()
        print('Exporting {}...'.format(rel_path), end='')

        export_path = get_export_path(source_path)
        ensure_directories(export_path.parent)

        options.infilename = source_path.resolve()
        options.outfilename = export_path.resolve()
        (input, output) = scour.getInOut(options)
        scour.start(options, input, output)

        print(' done')


if __name__ == '__main__':
    print('=================')
    print('Building icons...')
    print('=================')
    build()
