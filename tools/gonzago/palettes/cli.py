from pathlib import Path

import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

from .. import BASE_DIR_PATH, SOURCE_DIR_PATH

from .templates import Template, find_templates
from .formatters import ExporterInfo, EXPORTERS


PALETTES_SOURCE_DIR: Path = SOURCE_DIR_PATH.joinpath("./palettes").resolve()
PALETTES_DST_DIR: Path = BASE_DIR_PATH.joinpath("palettes").resolve()


app = typer.Typer()
console: Console = Console()


@app.command("save_template")
def save_template(name: str = "new_palette_template.yaml") -> None:
    """
    Save palette template.
    """
    file: Path = PALETTES_SOURCE_DIR.joinpath(name).resolve()
    template: Template = Template.default()
    template.save(file)


@app.command("templates")
def list_templates() -> None:
    """
    List valid palette templates.
    """
    if not PALETTES_SOURCE_DIR.exists():
        console.print(f"Path {PALETTES_SOURCE_DIR} does not exist!")
        return

    console.print(f"Searching templates at [i]{PALETTES_SOURCE_DIR}[/i]...")
    with console.status("Searching templates...") as status:
        valid_templates_count: int = 0
        table: Table = Table("Path", "Name", "Description", "Colors")
        for file in find_templates(PALETTES_SOURCE_DIR):
            rel_path: Path = file.relative_to(PALETTES_SOURCE_DIR)
            try:
                template: Template = Template.load(file)
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
            console.print(f"Found valid palette templates: {valid_templates_count}")
        else:
            console.print("No valid palette templates found!", style="yellow")
        if table.row_count > 0:
            console.print(table)


@app.command("exporters")
def list_exporters():
    """
    List available exporters.
    """
    count: int = len(EXPORTERS)
    if count == 0:
        console.print("No exporters available!", style="yellow")
        return
    console.print(f"Available exporters: {count}")
    table: Table = Table("ID", "Suffix", "Description")
    for id, (suffix, description, _) in EXPORTERS.items():
        table.add_row(id, suffix, description)
    console.print(table)


@app.command("readme")
def build_readme():
    """
    Build readme from all palettes.
    """

    if not PALETTES_SOURCE_DIR.exists():
        console.print(f"Path {PALETTES_SOURCE_DIR} does not exist!")
        return

    with console.status("Building readme...") as status:
        path: Path = PALETTES_DST_DIR.joinpath("README.md").resolve()
        with path.open("w") as readme:
            readme.write(
                "# Gonzago Framework Palettes\n\n"
                "Different palettes for use in Gonzago Framework and its design elements.\n\n"
            )

            readme.write(
                "## Formats\n\n"
                "<table>\n"
                "<thead><tr>"
                "<th align=\"left\">ID</th>"
                "<th align=\"left\">Suffix</th>"
                "<th align=\"left\">Description</th>"
                "</tr></thead>\n"
                "<tbody>\n"
            )
            for id, (suffix, description, _) in EXPORTERS.items():
                readme.write(
                    f"<tr><td>{id}</td><td>{suffix}</td><td>{description}</td></tr>\n"
                )
            readme.write(
                "</tbody>\n"
                "</table>\n\n"
            )

            readme.write(
                "## Palettes\n\n"
            )
            for file in find_templates(PALETTES_SOURCE_DIR):
                rel_path: Path = file.relative_to(PALETTES_SOURCE_DIR)
                console.print(rel_path)
                status.update(f"Exporting {rel_path}")
                try:
                    template: Template = Template.load(file)
                    readme.write(
                        f"### {template.name}\n\n"
                    )
                    if template.description:
                        readme.write(f"{template.description}\n\n")
                    readme.write(
                        "<table>\n"
                    )
                    if template.version:
                        readme.write(
                            f"<tr><th>Version</th><td>{template.version}</td></tr>\n"
                        )
                    if template.author:
                        readme.write(
                            f"<tr><th>Author</th><td>{template.author}</td></tr>\n"
                        )
                    if template.source:
                        readme.write(
                            f"<tr><th>Source</th><td>{template.source}</td></tr>\n"
                        )

                    readme.write(
                            "<tr>\n<th>Colors</th>\n<td>\n"
                        )
                    for entry in template.colors:
                        readme.write(
                            f"<p>{entry.name}"
                        )
                        if entry.description:
                            readme.write(
                                f"<br>{entry.description}"
                            )
                        readme.write(
                            f"<br>{entry.color}</p>"
                        )
                    readme.write(
                            "</td>\n</tr>\n"
                        )
                    readme.write(
                        "</table>\n\n"
                    )
                except Exception as e:
                    console.print(
                        f"{type(e).__name__}: {str(e)}" if e else "Export failed",
                        style="red",
                    )
            console.print("Done")


@app.command("build")
def build():
    """
    Build palettes in all formats.
    """
    if len(EXPORTERS.keys()) == 0:
        console.print(f"No exporters available!")
        return

    if not PALETTES_SOURCE_DIR.exists():
        console.print(f"Path {PALETTES_SOURCE_DIR} does not exist!")
        return

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        progress.add_task(description="Exec Command", total=None)

    console.print(f"Building palettes...")
    with console.status("Building templates...") as status:
        for file in find_templates(PALETTES_SOURCE_DIR):
            rel_path: Path = file.relative_to(PALETTES_SOURCE_DIR)
            console.print(rel_path)
            try:
                template: Template = Template.load(file)
                console.print(f"Exporting {template.name}")
                for exporter in EXPORTERS.keys():
                    exporter_info: ExporterInfo = EXPORTERS.get(exporter)
                    export_path: Path = PALETTES_DST_DIR.joinpath(rel_path).with_suffix(
                        exporter_info.suffix
                    )
                    export_path.parent.mkdir(
                        parents=True, exist_ok=True
                    )  # Ensure folders
                    status.update(f"Exporting {exporter} to [i]{export_path}[/i]")
                    exporter_info.fn(export_path, template)
                    console.print(f"Exported to [i]{export_path}[/i]")
            except Exception as e:
                console.print(
                    f"{type(e).__name__}: {str(e)}" if e else "Export failed",
                    style="red",
                )
        console.print("Done")


@app.callback(invoke_without_command=True)
def main(ctx: typer.Context) -> None:
    """
    Color palette tools.
    """
    if ctx.invoked_subcommand is None:
        console.print("Initializing database")
        console.print(
            Panel("Hello, [red]World!", title="Welcome", subtitle="Thank you")
        )


if __name__ == "__main__":
    app()
