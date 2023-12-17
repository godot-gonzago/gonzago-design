from pathlib import Path
from shutil import rmtree
from tomlkit import TOMLDocument, dumps, parse

import typer

from gonzago import __app_name__

APP_DIR: Path = Path(typer.get_app_dir(__app_name__)).resolve()
CONFIG_FILE: Path = APP_DIR.joinpath("config.toml").resolve()


def exists() -> bool:
    return CONFIG_FILE.is_file()


def load() -> TOMLDocument:
    return parse(
        CONFIG_FILE.read_text() if CONFIG_FILE.is_file() else (
            '[paths]\n'
            f'dst = "{Path(__file__).joinpath("../../..").resolve().as_posix()}"\n'
            f'src = "{Path(__file__).joinpath("../../../source").resolve().as_posix()}"\n'
            '\n'
            '[inkscape]\n'
            'path = ""\n'
            '\n'
            '[blender]\n'
            'path = ""'
        )
    )


def save(config: TOMLDocument) -> None:
    CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)  # Ensure folders
    CONFIG_FILE.write_text(dumps(config))


def clear() -> None:
    if APP_DIR.exists():
        rmtree(APP_DIR)


CONFIG: TOMLDocument = load()


# Inkscape C:\Program Files\Inkscape\bin\inkscape.exe
# C:\Program Files\Blender Foundation\Blender 4.0\blender.exe
#
# Linux /usr/lib/blender
# Win %ProgramFiles%/Inkscape/bin/inkscape.exe
# OSX /Applications/Blender/blender.app/Contents/MacOS/blender
