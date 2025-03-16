from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console

from gonzago.core.config import CONFIG
from gonzago.core.palettes.io import get_palette_file
from gonzago.core.palettes.parsing import PaletteWriter

PALETTES_SOURCE_DIR: Path = CONFIG.src_path("./palettes")
PALETTES_DST_DIR: Path = CONFIG.dst_path("palettes")


console: Console = Console()


def import_palette(
    path: Annotated[
        Path,
        typer.Option(
            "--file",
            "-f",
            help="File to import.",
            exists=True,
            file_okay=True,
            dir_okay=False,
            readable=True,
            resolve_path=True,
            # prompt=True
        ),
    ],
) -> None:
    """
    Import a palette from a file.
    """
    try:
        file = get_palette_file(path)
        file.read()
        file_out = file.create_output_file(
            PALETTES_SOURCE_DIR, PaletteWriter.get_writer_from_id("template")
        )
        file_out.write()
        console.print(file_out.as_posix())
    except Exception:
        console.print_exception()
        # console.print(e, style="red")
