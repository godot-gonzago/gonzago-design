from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.table import Table

from .io import Palette, Writer, get_readers, get_writers, find_palettes, read, write

from .. import BASE_DIR_PATH, SOURCE_DIR_PATH


PALETTES_SOURCE_DIR: Path = SOURCE_DIR_PATH.joinpath("./palettes").resolve()
PALETTES_DST_DIR: Path = BASE_DIR_PATH.joinpath("palettes").resolve()


app = typer.Typer()
console: Console = Console()


@app.command("writers")
def list_writers():
    table: Table = Table("ID", "Suffix", "Description")
    for writer in get_writers():
        table.add_row(writer.id, writer.suffix, writer.description)
    if table.row_count > 0:
        console.print(table)
    else:
        console.print("No writers available!", style="yellow")


@app.command("readers")
def list_readers():
    table: Table = Table("ID", "Pattern", "Description")
    for reader in get_readers():
        table.add_row(reader.id, reader.pattern, reader.description)
    if table.row_count > 0:
        console.print(table)
    else:
        console.print("No readers available!", style="yellow")


@app.command("new")
def new(
    file: Path = "new_palette_template.yaml", name: str = "New Palette Template"
) -> None:
    """
    Create new palette template.
    """
    # if not file.is_absolute():
    #     file = PALETTES_SOURCE_DIR.joinpath(file)
    # file = file.resolve()
    # if not file.match(TEMPLATE_FILE_PATTERN):
    #     console.print(f"[i]{file}[/i] is not a valid template path!", style="red")
    #     return

    # if file.exists():
    #     typer.confirm("File already exists! Override?", abort=True)

    # data: dict = {
    #     "name": name if name and len(name) > 0 else "New Palette Template",
    #     "description": "A brand new palette template.",
    #     "version": Version(1, 0, 0),
    #     "author": "David Krummenacher and Gonzago Framework contributors",
    #     "source": "https://github.com/godot-gonzago/gonzago-design",
    #     "colors": [
    #         {
    #             "name": "Black",
    #             "description": "Black is an achromatic color.",
    #             "color": Color("black"),
    #         },
    #         {
    #             "name": "White",
    #             "description": "White is an achromatic color.",
    #             "color": Color("white"),
    #         },
    #     ],
    # }

    # template: Template = Template.model_validate(data)
    # json: dict = Template.model_dump(template, mode="json")

    # file.parent.mkdir(parents=True, exist_ok=True)  # Ensure folders
    # with file.open("w") as stream:
    #     yaml.safe_dump(json, stream, sort_keys=False)
    # console.print(f"Created template file: [i]{file}[/i]", style="green")
    pass


@app.command("check")
def check(path: Path = PALETTES_SOURCE_DIR) -> None:
    """
    Validate palette templates.
    """
    pass


@app.command("ls")
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
                    template.name,
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


# src_path: Annotated[
#     Optional[Path],
#     typer.Option(
#         "--in",
#         "-i",
#         help="Input template file or directory.",
#         exists=True,
#         file_okay=True,
#         dir_okay=True,
#         readable=True,
#         resolve_path=True,
#         # show_default=False,
#     ),
# ] = PALETTES_SOURCE_DIR,
# out_dir: Annotated[
#     Optional[Path],
#     typer.Option(
#         "--out",
#         "-o",
#         help="Palettes output directory.",
#         file_okay=False,
#         dir_okay=True,
#         writable=True,
#         resolve_path=True,
#         # show_default=False,
#     ),
# ] = PALETTES_DST_DIR,
# exporters: Annotated[
#     Optional[List[str]],
#     typer.Option("--export", "-e", help="List of exporters to use."),
# ] = list[str](EXPORTERS.keys()),


@app.command("publish")
def publish(
    src: Path = PALETTES_SOURCE_DIR,
    dst_dir: Path = PALETTES_DST_DIR,
    formats: list[str] = [w.id for w in get_writers()],
) -> None:
    """
    Publish palettes in specified formats.
    """
    # if src == None:
    #     src = PALETTES_SOURCE_DIR
    # elif not src.is_absolute():
    #     src = PALETTES_SOURCE_DIR.joinpath(src)
    # src = src.resolve()
    # if not src.exists():
    #     console.print(f"Path {PALETTES_SOURCE_DIR} does not exist!", style="red")
    #     return

    # if dst_dir == None:
    #     dst_dir = PALETTES_DST_DIR
    # elif not dst_dir.is_absolute():
    #     dst_dir = PALETTES_DST_DIR.joinpath(dst_dir)
    # dst_dir = dst_dir.resolve()
    # if not dst_dir.is_dir():
    #     console.print(f"Destination {PALETTES_SOURCE_DIR} is not a folder!", style="red")
    #     return

    # if len(FORMATTERS.keys()) == 0:
    #     console.print(f"No exporters available!", style="red")
    #     return

    writers: list[Writer] = list(get_writers(True))
    # formatters: list[str] = []
    # for format in formats:
    #     if not format in formatters:
    #         if not format in FORMATTERS.keys():
    #             console.print(f"Format [i]{format}[/i] not supported!", style="yellow")
    #             continue
    #         formatters.append(format)

    # if len(formatters) == 0:
    #     console.print(f"No supported formats!", style="yellow")
    #     return

    for file in find_palettes(src):
        rel_path: Path = file.relative_to(src)
        console.print(f"Exporting '{rel_path.as_posix()}'...")
        palette: Palette
        try:
            palette = read(file)
        except Exception as e:
            console.print(
                f"{type(e).__name__}: {str(e)}" if e else "Palette load failed",
                style="red",
            )
            continue
        for writer in writers:
            try:
                export_path: Path = PALETTES_DST_DIR.joinpath(rel_path).with_suffix(
                    writer.suffix
                )
                export_path.parent.mkdir(parents=True, exist_ok=True)  # Ensure folders
                write(writer.id, export_path, palette)
                console.print(
                    f"Exported '[i]{export_path.relative_to(dst_dir).as_posix()}[/i]'"
                )
            except Exception as e:
                console.print(
                    f"{type(e).__name__}: {str(e)}" if e else "Export of failed",
                    style="red",
                )
                continue
    console.print("Done")


@app.command("readme")
def build_readme(src_dir: Path = PALETTES_SOURCE_DIR, dst_dir: Path = PALETTES_DST_DIR):
    """
    Build readme from all palettes.
    """
    #     """
    #     Build readme from all palettes.
    #     """

    #     if not PALETTES_SOURCE_DIR.exists():
    #         console.print(f"Path {PALETTES_SOURCE_DIR} does not exist!")
    #         return

    #     with console.status("Building readme...") as status:
    #         path: Path = PALETTES_DST_DIR.joinpath("README.md").resolve()
    #         with path.open("w") as readme:
    #             readme.write(
    #                 "# Gonzago Framework Palettes\n\n"
    #                 "Different palettes for use in Gonzago Framework and its design elements.\n\n"
    #             )

    #             readme.write(
    #                 "## Formats\n\n"
    #                 "<table>\n"
    #                 "<thead><tr>"
    #                 "<th align=\"left\">ID</th>"
    #                 "<th align=\"left\">Suffix</th>"
    #                 "<th align=\"left\">Description</th>"
    #                 "</tr></thead>\n"
    #                 "<tbody>\n"
    #             )
    #             for id, (suffix, description, _) in FORMATTERS.items():
    #                 readme.write(
    #                     f"<tr><td>{id}</td><td>{suffix}</td><td>{description}</td></tr>\n"
    #                 )
    #             readme.write(
    #                 "</tbody>\n"
    #                 "</table>\n\n"
    #             )

    #             readme.write(
    #                 "## Palettes\n\n"
    #             )
    #             for file in find_templates(PALETTES_SOURCE_DIR):
    #                 rel_path: Path = file.relative_to(PALETTES_SOURCE_DIR)
    #                 console.print(rel_path)
    #                 status.update(f"Exporting {rel_path}")
    #                 try:
    #                     template: Template = Template.load(file)
    #                     readme.write(
    #                         f"### {template.name}\n\n"
    #                     )
    #                     if template.description:
    #                         readme.write(f"{template.description}\n\n")
    #                     readme.write(
    #                         "<table>\n"
    #                     )
    #                     if template.version:
    #                         readme.write(
    #                             f"<tr><th>Version</th><td>{template.version}</td></tr>\n"
    #                         )
    #                     if template.author:
    #                         readme.write(
    #                             f"<tr><th>Author</th><td>{template.author}</td></tr>\n"
    #                         )
    #                     if template.source:
    #                         readme.write(
    #                             f"<tr><th>Source</th><td>{template.source}</td></tr>\n"
    #                         )

    #                     readme.write(
    #                             "<tr>\n<th>Colors</th>\n<td>\n"
    #                         )
    #                     for entry in template.colors:
    #                         readme.write(
    #                             f"<p>{entry.name}\n"
    #                         )
    #                         if entry.description:
    #                             readme.write(
    #                                 f"<br>{entry.description}\n"
    #                             )
    #                         readme.write("<br>")
    #                         c = entry.color.as_rgb_tuple()
    #                         hex: str = f"{c[0]:02x}{c[1]:02x}{c[2]:02x}"
    #                         readme.write(
    #                             f"<img src=\"https://placehold.co/24x24/{hex}/{hex}/png\" /> #{hex}"
    #                         )
    #                     readme.write(
    #                             "</td>\n</tr>\n"
    #                         )
    #                     readme.write(
    #                         "</table>\n\n"
    #                     )
    #                 except Exception as e:
    #                     console.print(
    #                         f"{type(e).__name__}: {str(e)}" if e else "Export failed",
    #                         style="red",
    #                     )
    #             console.print("Done")
    pass


# @app.callback(invoke_without_command=True)
# def main(ctx: typer.Context) -> None:
#     """
#     Color palette tools.
#     """
#     if ctx.invoked_subcommand is None:
#         console.print("Initializing database")
#         console.print(
#             Panel("Hello, [red]World!", title="Welcome", subtitle="Thank you")
#         )


@app.callback(no_args_is_help=True)
def main() -> None:
    """
    Color palette tools.
    """
    pass


if __name__ == "__main__":
    app()
