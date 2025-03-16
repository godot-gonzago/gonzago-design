from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console

from gonzago.core.config import CONFIG
from gonzago.core.icons.io import find_icons

ICONS_SOURCE_DIR: Path = CONFIG.src_path("./engine/editor_icons")
ICONS_DST_DIR: Path = CONFIG.dst_path("icons")


console: Console = Console()


def list(
    path: Annotated[
        Path,
        typer.Option(
            help="The path to start looking for icons. Defaults to icon source directory"
        ),
    ] = ICONS_SOURCE_DIR,
):
    """
    Print relative icon file paths at given path. Default path is icons source directory.
    """
    for file in find_icons(path):
        rel_path: Path = file.relative_to(path)
        console.print(f"{rel_path}")
