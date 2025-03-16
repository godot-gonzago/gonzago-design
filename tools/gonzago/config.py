import sys
from pathlib import Path
from shutil import rmtree

import tomlkit
import typer

from gonzago import __app_name__

APP_DIR: Path = Path(typer.get_app_dir(__app_name__)).resolve()
CONFIG_FILE: Path = APP_DIR.joinpath("config.toml").resolve()


def build_default() -> tomlkit.TOMLDocument:
    doc = tomlkit.document()
    doc.add(tomlkit.comment(__app_name__))
    doc.add(tomlkit.nl())

    dst = Path(__file__).joinpath("../../..").resolve()
    src = dst.joinpath("source").resolve()

    paths = tomlkit.table()
    paths.add("dst", dst.as_posix())
    paths.add("src", src.as_posix())
    doc.add("paths", paths)
    doc.add(tomlkit.nl())

    io = tomlkit.table()
    io.add("max_depth", 8)
    doc.add("io", io)
    doc.add(tomlkit.nl())

    inkscape_path = "inkscape"
    if sys.platform.startswith("linux"):
        inkscape_path = "/usr/lib/inkscape"
    elif sys.platform.startswith("win32"):
        inkscape_path = "%ProgramFiles%/Inkscape/bin/inkscape.exe"
    elif sys.platform.startswith("darwin"):
        inkscape_path = "/Applications/Inkscape.app/Contents/MacOS/inkscape"

    inkscape = tomlkit.table()
    inkscape.add("path", inkscape_path)
    doc.add("inkscape", inkscape)
    doc.add(tomlkit.nl())

    blender_path = "blender"
    if sys.platform.startswith("linux"):
        blender_path = "/usr/lib/blender"
    elif sys.platform.startswith("win32"):
        blender_path = "%ProgramFiles%/Blender Foundation/Blender 4.0/blender.exe"
    elif sys.platform.startswith("darwin"):
        blender_path = "/Applications/Blender/blender.app/Contents/MacOS/blender"

    blender = tomlkit.table()
    blender.add("path", blender_path)
    doc.add("blender", blender)
    doc.add(tomlkit.nl())

    return doc


def exists() -> bool:
    return CONFIG_FILE.is_file()


def load() -> tomlkit.TOMLDocument:
    doc = build_default()
    if exists():
        persitent = tomlkit.parse(CONFIG_FILE.read_text())
        doc.update(persitent)
    return doc


def save(config: tomlkit.TOMLDocument) -> None:
    CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)  # Ensure folders
    CONFIG_FILE.write_text(tomlkit.dumps(config))


def clear() -> None:
    if APP_DIR.exists():
        rmtree(APP_DIR)


CONFIG: tomlkit.TOMLDocument = load()


def src_path(rel: Path | str) -> Path:
    return Path(CONFIG["paths"]["src"]).joinpath(rel).resolve()


def dst_path(rel: Path | str) -> Path:
    return Path(CONFIG["paths"]["dst"]).joinpath(rel).resolve()
