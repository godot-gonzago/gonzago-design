from pathlib import Path
from typing import Annotated

from jinja2 import Environment, FileSystemLoader, Template
import typer
from rich.console import Console
from rich.table import Table

from ..utils import snake_case
from ..config import dst_path, src_path
from .models import (
    Palette,
    generate_default_palette,
)
from .parsing import (
    Writer,
    get_readers,
    get_writers,
    get_writer_from_id,
)
from .io import get_palette_file, get_palette_files

PALETTES_SOURCE_DIR: Path = src_path("./palettes")
PALETTES_DST_DIR: Path = dst_path("palettes")


app = typer.Typer()
console: Console = Console()


@app.command("writers")
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
    for writer in get_writers(external, internal):
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


@app.command("readers")
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
    for reader in get_readers(external, internal):
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


@app.command("create")
def create_new_template(
    title: str = "New Palette Template",
    # depth: GenerationDepth,
) -> None:
    """
    Create new palette template.
    """

    file: Path = PALETTES_SOURCE_DIR.joinpath(snake_case(title) + ".yaml")
    if file.exists():
        typer.confirm("File already exists! Override?", abort=True)

    palette: Palette = generate_default_palette(title)
    writer = get_writer_from_id("template")
    writer.write(palette, file)

    console.print(f"Created template file: [i]{file}[/i]", style="green")


@app.command("import")
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
        file_out = file.create_output_file(PALETTES_SOURCE_DIR, get_writer_from_id("template"))
        file_out.write()
        console.print(file_out.as_posix())
    except Exception as e:
        console.print_exception()
        #console.print(e, style="red")


@app.command("list")
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


# TODO: https://typer.tiangolo.com/tutorial/progressbar/#spinner
# TODO: https://typer.tiangolo.com/tutorial/progressbar/#progress-bar_1
# TODO: https://rich.readthedocs.io/en/stable/progress.html#basic-usage
@app.command("publish")
def publish() -> None:
    """
    Publish palettes in full.
    """

    console.print("Gathering export formats")
    formats: list[Writer] = list(get_writers())

    console.print("Gathering palettes")
    palettes: list[Palette] = list()
    for file in get_palette_files(PALETTES_SOURCE_DIR):
        console.print(f"Reading [i]'{file.as_posix()}'[/i]...")
        palette: Palette
        try:
            palette = file.read()
            palettes.append(palette)
        except Exception as e:
            console.print(e, style="red")
            continue

        console.print(f"Exporting [i]'{file.as_posix()}'[/i]...")
        for format in formats:
            try:
                file_out = file.create_output_file(PALETTES_DST_DIR, format)
                file_out.write()
                console.print(f"Exported [i]'{file_out.as_posix()}'[/i]")
            except Exception as e:
                console.print(e, style="red")
                continue

    console.status("Building [i]'README.md'[/i]...")

    environment: Environment = Environment(loader=FileSystemLoader(PALETTES_SOURCE_DIR))
    environment.trim_blocks = True
    environment.lstrip_blocks = True
    template: Template = environment.get_template("README.md.jinja")
    content: str = template.render(formats=formats, palettes=palettes)

    console.status("Writing [i]'README.md'[/i]...")
    path: Path = PALETTES_DST_DIR.joinpath("README.md").resolve()
    path.write_text(content)

    console.print("Done")


# TODO: COPYRIGHT.txt https://www.debian.org/doc/packaging-manuals/copyright-format/1.0/
# CHANGELOG.md
# CONTRIBUTING.md
# AUTHORS.md
# SUPPORT.md
# ACKNOWLEDGMENTS.md
# https://github.com/kmindi/special-files-in-repository-root/blob/master/README.md


@app.callback(no_args_is_help=True)
def main() -> None:
    """
    Color palette tools.
    """
    pass


if __name__ == "__main__":
    app()
