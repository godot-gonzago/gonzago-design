from pathlib import Path
from gonzago import __app_name__
import typer

CONFIG_DIR_PATH: Path = Path(typer.get_app_dir(__app_name__)).resolve()
CONFIG_FILE_PATH: Path = CONFIG_DIR_PATH.joinpath("config.toml").resolve()

BASE_DIR_PATH: Path = Path(__file__).joinpath("../../..").resolve()
SOURCE_DIR_PATH: Path = BASE_DIR_PATH.joinpath("source").resolve()

# Inkscape C:\Program Files\Inkscape\bin\inkscape.exe
# C:\Program Files\Blender Foundation\Blender 4.0\blender.exe
#
# Linux /usr/lib/blender
# Win %ProgramFiles%/Inkscape/bin/inkscape.exe
# OSX /Applications/Blender/blender.app/Contents/MacOS/blender
