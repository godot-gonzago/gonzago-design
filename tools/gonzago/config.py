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
    if CONFIG_FILE.is_file():
        return parse(CONFIG_FILE.read_text())

    dst: Path = Path(__file__).joinpath("../../..").resolve()
    src: Path = dst.joinpath("source").resolve()
    inkscape: str = ""
    # Linux /usr/lib/inkscape
    # Win %ProgramFiles%/Inkscape/bin/inkscape.exe
    # OSX /Applications/Inkscape.app/Contents/MacOS/inkscape
    blender: str = ""
    # Linux /usr/lib/blender
    # Win %ProgramFiles%/Blender Foundation/Blender 4.0/blender.exe
    # OSX /Applications/Blender/blender.app/Contents/MacOS/blender
    return parse((
        '[paths]\n'
        f'dst = "{dst.as_posix()}"\n'
        f'src = "{src.as_posix()}"\n'
        '\n'
        '[inkscape]\n'
        f'path = "{inkscape}"\n'
        '\n'
        '[blender]\n'
        f'path = "{blender}"'
    ))


def save(config: TOMLDocument) -> None:
    CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)  # Ensure folders
    CONFIG_FILE.write_text(dumps(config))


def clear() -> None:
    if APP_DIR.exists():
        rmtree(APP_DIR)


CONFIG: TOMLDocument = load()
