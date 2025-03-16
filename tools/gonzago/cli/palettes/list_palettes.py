from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console
from rich.table import Table

from gonzago.core.config import CONFIG
from gonzago.core.palettes.io import get_palette_files

PALETTES_SOURCE_DIR: Path = CONFIG.src_path("./palettes")
PALETTES_DST_DIR: Path = CONFIG.dst_path("palettes")


console: Console = Console()


def list_palettes(
    dir: Annotated[
        Path,
        typer.Option(
            "--dir",
            "-d",
            help="Directory to search for palettes.",
            exists=True,
            file_okay=False,
            dir_okay=True,
            readable=True,
            resolve_path=True,
        ),
    ] = PALETTES_SOURCE_DIR,
) -> None:
    """
    List palette templates.
    """
    if not dir.exists():
        console.print(f"Path [i]{dir}[/i] does not exist!", style="yellow")
        return

    with console.status(f"Searching templates at [i]{dir}[/i]...") as status:
        valid_templates_count: int = 0
        table: Table = Table("Path", "Name", "Description", "Colors")

        for file in get_palette_files(dir):
            status.update()
            try:
                template = file.read()
                table.add_row(
                    file.as_posix(),
                    template.title,
                    template.description if template.description else "",
                    str(len(template.colors)),
                )
                valid_templates_count += 1
            except Exception as e:
                table.add_row(
                    file.as_posix(),
                    "Unknown",
                    f"{type(e).__name__}: {str(e)}" if e else "Template is invalid.",
                    "-",
                    style="red",
                )
        if valid_templates_count > 0:
            console.print(f"Found {valid_templates_count} valid palette templates!")
        else:
            console.print("No valid palette templates found!", style="yellow")
        if table.row_count > 0:
            console.print(table)
