from pathlib import Path

import typer
from rich.console import Console

from gonzago.core.config import CONFIG
from gonzago.core.palettes.models import Palette
from gonzago.core.palettes.parsing import PaletteWriter
from gonzago.core.utils import snake_case

PALETTES_SOURCE_DIR: Path = CONFIG.src_path("./palettes")
PALETTES_DST_DIR: Path = CONFIG.dst_path("palettes")


console: Console = Console()


def create(
    title: str = "New Palette Template",
    # depth: GenerationDepth,
) -> None:
    """
    Create new palette template.
    """

    file: Path = PALETTES_SOURCE_DIR.joinpath(snake_case(title) + ".yaml")
    if file.exists():
        typer.confirm("File already exists! Override?", abort=True)

    palette: Palette = Palette.generate_default(title)
    writer = PaletteWriter.get_writer_from_id("template")
    writer.write(palette, file)

    console.print(f"Created template file: [i]{file}[/i]", style="green")
