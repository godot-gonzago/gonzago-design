from typing import Annotated

import typer
from rich.console import Console
from rich.table import Table

from gonzago.core.palettes.parsing import PaletteWriter

console: Console = Console()


def list_writers(
    external: Annotated[
        bool,
        typer.Option(
            "--external/--no_external",
            help="List external palette writers.",
        ),
    ] = True,
    internal: Annotated[
        bool,
        typer.Option(
            "--internal/--no_internal",
            "-i",
            help="List internal palette writers.",
        ),
    ] = False,
):
    """
    List available palette format writers.
    """
    table: Table = Table("ID", "Suffix", "Description")
    for writer in PaletteWriter.get_writers(external, internal):
        if not writer.internal:
            table.add_row(writer.id, writer.suffix, writer.description)
        else:
            table.add_row(
                writer.id + " (internal)",
                writer.suffix,
                writer.description,
                style="bright_black",
            )
    if table.row_count > 0:
        console.print(table)
    else:
        console.print("No writers available!", style="yellow")
