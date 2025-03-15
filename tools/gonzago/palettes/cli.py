from pathlib import Path
from typing import Annotated, Iterable, List, Optional

from jinja2 import Environment, FileSystemLoader, Template
import typer
from rich.console import Console
from rich.table import Table

from ..config import dst_path, src_path
from .core import (
    Palette,
    generate_default_palette,
    get_readers,
    get_writers,
    get_writer_from_id,
)
from .io import (
    Writer,
    read,
    find_palettes,
)

PALETTES_SOURCE_DIR: Path = src_path("./palettes")
PALETTES_DST_DIR: Path = dst_path("palettes")


app = typer.Typer()
console: Console = Console()


@app.command("writers")
def list_writers(
    include_internal: Annotated[
        bool,
        typer.Option(
            "--include_internal/--exlude_internal",
            "-i",
            help="Include internal palette writers.",
        ),
    ] = False,
):
    """
    List all available palette format writers.
    """
    table: Table = Table("ID", "Suffix", "Description")
    for writer in get_writers(include_internal):
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
    include_internal: Annotated[
        bool,
        typer.Option(
            "--include_internal/--exlude_internal",
            "-i",
            help="Include internal palette readers.",
        ),
    ] = False,
):
    """
    List all available palette format readers.
    """
    table: Table = Table("ID", "Pattern", "Description")
    for reader in get_readers(include_internal):
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
    file: Path = "new_palette_template.yaml",
    title: str = "New Palette Template",
    format: str = "template",
) -> None:
    """
    Create new palette template.
    """
    if not file.is_absolute():
        file = PALETTES_SOURCE_DIR.joinpath(file)
    file = file.resolve()

    # if not file.match(TEMPLATE_FILE_PATTERN):
    #     console.print(f"[i]{file}[/i] is not a valid template path!", style="red")
    #     return

    if file.exists():
        typer.confirm("File already exists! Override?", abort=True)

    palette: Palette = generate_default_palette(title)
    writer = get_writer_from_id(format)
    writer.write(palette, file)

    console.print(f"Created template file: [i]{file}[/i]", style="green")


@app.command("import")
def import_palette(file: Path) -> None:
    """
    Validate palette templates.
    """
    pass


@app.command("list")
def list_palettes(dir: Path = PALETTES_SOURCE_DIR) -> None:
    """
    List palette templates.
    """
    if not dir.exists():
        console.print(f"Path [i]{dir}[/i] does not exist!", style="yellow")
        return

    with console.status(f"Searching templates at [i]{dir}[/i]...") as status:
        valid_templates_count: int = 0
        table: Table = Table("Path", "Name", "Description", "Colors")
        for file in find_palettes(dir):
            status.update()
            rel_path: str = file.relative_to(dir).as_posix()
            try:
                template = read(file)
                table.add_row(
                    str(rel_path),
                    template.title,
                    template.description if template.description else "",
                    str(len(template.colors)),
                )
                valid_templates_count += 1
            except Exception as e:
                table.add_row(
                    str(rel_path),
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


# Merge with publish
@app.command("export")
def export_palettes(
    src: Annotated[
        Path,
        typer.Option(
            "--in",
            "-i",
            help="Input template file or directory.",
            exists=True,
            file_okay=True,
            dir_okay=True,
            readable=True,
            resolve_path=True,
        ),
    ] = PALETTES_SOURCE_DIR,
    dst_dir: Annotated[
        Path,
        typer.Option(
            "--out",
            "-o",
            help="Palettes output directory.",
            file_okay=False,
            dir_okay=True,
            writable=True,
            resolve_path=True,
        ),
    ] = PALETTES_DST_DIR,
    formats: Annotated[
        list[str], typer.Option("--export", "-e", help="List of exporters to use.")
    ] = [w.id for w in get_writers()],
) -> None:
    """
    Export palettes in specified formats.
    """
    for file in find_palettes(src):
        rel_path: Path = file.relative_to(src)
        console.print(f"Exporting '{rel_path.as_posix()}'...")

        palette: Palette
        try:
            palette = read(file)
        except Exception as e:
            console.print(
                (
                    f"Palette load failed: {type(e).__name__}: {str(e)}"
                    if e
                    else "Palette load failed!"
                ),
                style="red",
            )
            continue

        export_base_path: Path = dst_dir.joinpath(rel_path).resolve()
        for id in formats:
            try:
                writer: Writer = get_writer_from_id(id)
                export_path: Path = writer.build_file_path(export_base_path)
                export_rel_path: Path = export_path.relative_to(dst_dir)
                writer.write(palette, export_path)
                console.print(f"Exported '[i]{export_rel_path.as_posix()}[/i]'")
            except Exception as e:
                console.print(
                    (
                        f"Export '{id}' failed: {type(e).__name__}: {str(e)}"
                        if e
                        else f"Export '{id}' failed!"
                    ),
                    style="red",
                )
                continue
    console.print("Done")


# Merge with publish
@app.command("readme")
def build_readme(src_dir: Path = PALETTES_SOURCE_DIR, dst_dir: Path = PALETTES_DST_DIR):
    """
    Build readme from all palettes.
    """
    console.status("Building readme...")

    environment: Environment = Environment(loader=FileSystemLoader(src_dir))
    environment.trim_blocks = True
    environment.lstrip_blocks = True
    template: Template = environment.get_template("README.md.jinja")
    formats: list[Writer] = list(get_writers())
    palettes: list[Palette] = list()

    for file in find_palettes(src_dir):
        rel_path: Path = file.relative_to(src_dir)
        console.print(f"Reading '{rel_path.as_posix()}'...")
        palette: Palette
        try:
            palette = read(file)
            palettes.append(palette)
        except Exception as e:
            console.print(
                (
                    f"Palette reading failed: {type(e).__name__}: {str(e)}"
                    if e
                    else "Palette reading failed!"
                ),
                style="red",
            )
            continue

    content: str = template.render(formats=formats, palettes=palettes)
    path: Path = dst_dir.joinpath("README.md").resolve()
    path.write_text(content)

    console.print("Done")


# TODO: Externalize steps to allow for better commands.
#def _gather_formats(include_internal: bool = False) -> List[Writer]:
#    console.print("Gathering export formats")
#    return list[get_writers(include_internal)]
#
#def _gather_palettes() -> None:
#    pass
#
#def _export_palettes(formats: List[Writer]) -> None:
#    pass
#
#def _create_readme(src_dir: Path, dst_dir: Path, formats: List[Writer], palettes: list[Palette]) -> None:
#    console.status("Building [i]'README.md'[/i]...")
#
#    environment: Environment = Environment(loader=FileSystemLoader(src_dir))
#    environment.trim_blocks = True
#    environment.lstrip_blocks = True
#    template: Template = environment.get_template("README.md.jinja")
#    content: str = template.render(formats=formats, palettes=palettes)
#
#    console.status("Writing [i]'README.md'[/i]...")
#    path: Path = dst_dir.joinpath("README.md").resolve()
#    path.write_text(content)
#
#    console.print("Done")


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
    for file in find_palettes(PALETTES_SOURCE_DIR):
        rel_path: Path = file.relative_to(PALETTES_SOURCE_DIR)
        console.print(f"Reading [i]'{rel_path.as_posix()}'[/i]...")
        palette: Palette
        try:
            palette = read(file)
            palettes.append(palette)
        except Exception as e:
            console.print(e, style="red")
            continue

        console.print(f"Exporting [i]'{rel_path.as_posix()}'[/i]...")
        export_base_path: Path = PALETTES_DST_DIR.joinpath(rel_path).resolve()
        for format in formats:
            try:
                export_path: Path = format.build_file_path(export_base_path)
                export_rel_path: Path = export_path.relative_to(PALETTES_DST_DIR)
                format.write(palette, export_path)
                console.print(f"Exported [i]'{export_rel_path.as_posix()}'[/i]")
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
