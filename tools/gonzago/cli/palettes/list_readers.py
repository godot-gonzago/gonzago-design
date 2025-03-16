from typing import Annotated

import typer
from rich.console import Console
from rich.table import Table

from gonzago.core.palettes.parsing import PaletteReader

console: Console = Console()


def list_readers(
    external: Annotated[
        bool,
        typer.Option(
            "--external/--no_external",
            help="List external palette readers.",
        ),
    ] = True,
    internal: Annotated[
        bool,
        typer.Option(
            "--internal/--no_internal",
            "-i",
            help="List internal palette readers.",
        ),
    ] = False,
):
    """
    List available palette format readers.
    """
    table: Table = Table("ID", "Pattern", "Description")
    for reader in PaletteReader.get_readers(external, internal):
        if not reader.internal:
            table.add_row(reader.id, reader.pattern, reader.description)
        else:
            table.add_row(
                reader.id + " (internal)",
                reader.pattern,
                reader.description,
                style="bright_black",
            )
    if table.row_count > 0:
        console.print(table)
    else:
        console.print("No readers available!", style="yellow")
