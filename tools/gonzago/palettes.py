from pathlib import Path
from typing import (
    Callable,
    List,
    NamedTuple,
    Optional
)

import typer
import yaml
from pydantic import BaseModel
from pydantic_extra_types.color import Color
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

from gonzago import BASE_DIR_PATH, SOURCE_DIR_PATH
from gonzago.pydantic import Version


PALETTES_SOURCE_DIR: Path = SOURCE_DIR_PATH.joinpath("./palettes").resolve()
PALETTES_DST_DIR: Path = BASE_DIR_PATH.joinpath("palettes").resolve()


app = typer.Typer()
console: Console = Console()


TEMPLATE_FILE_PATTERN: str = "**/*.y[a]ml"


class TemplateEntry(BaseModel):
    name: str
    description: Optional[str] = None
    color: Color


class Template(BaseModel):
    name: str
    description: Optional[str] = None
    version: Optional[Version] = None
    author: Optional[str] = None
    source: Optional[str] = None
    colors: List[TemplateEntry]


    @classmethod
    def default(cls, name: str = "New Palette Template"):
        data: dict = {
            "name": name,
            "description": "A brand new palette template.",
            "version": Version(1, 0, 0),
            "author": "David Krummenacher and Gonzago Framework contributors",
            "source": "https://github.com/godot-gonzago/gonzago-design",
            "colors": [{
                "name": "Black",
                "description": "Black is an achromatic color.",
                "color": Color("black")
            },{
                "name": "White",
                "description": "White is an achromatic color.",
                "color": Color("white")
            }]
        }
        return cls.model_validate(data)


    @classmethod
    def load(cls, file: Path):
        if not file.match(TEMPLATE_FILE_PATTERN) or not file.is_file():
            raise TypeError("Not a valid template path")
        with file.open() as stream:
            data: dict = yaml.safe_load(stream)
            return cls.model_validate(data)


    def save(self, file: Path) -> None:
        if not file.match(TEMPLATE_FILE_PATTERN):
            raise TypeError(f"{file} is not a valid template path")
        data: dict = Template.model_dump(self, mode="json")
        file.parent.mkdir(parents=True, exist_ok=True) # Ensure folders
        with file.open("w") as stream:
            yaml.safe_dump(data, stream, sort_keys=False)


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
        for file in PALETTES_SOURCE_DIR.glob(TEMPLATE_FILE_PATTERN):
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


class ExporterInfo(NamedTuple):
    suffix: str
    description: str
    fn: Callable[[Path, Template], None]


EXPORTERS = dict[str, ExporterInfo]()


def exporter(id: str, suffix: str, description: str = "") -> Callable:
    def inner(fn: Callable[[Path, Template], None]) -> Callable[[Path, Template], None]:
        EXPORTERS[id] = ExporterInfo(suffix=suffix, description=description, fn=fn)
        return fn

    return inner


@exporter("png", ".png", "PNG palette image with size 1px.")
def export_png(out_file: Path, template: Template, size: int = 1) -> None:
    """
    PNG

    PNG palette image with size 1px.
    """
    from PIL import Image, ImageDraw

    color_count: int = len(template.colors)
    image: Image = Image.new("RGB", (color_count * size, size))

    draw = ImageDraw.Draw(image, "RGB")
    for i in range(color_count):
        color = template.colors[i].color
        draw.rectangle((i * size, 0, i * size + size, size), color.as_rgb_tuple())

    image.save(out_file, "PNG")


@exporter("png-8", ".x8.png", "PNG palette image with size 8px.")
def export_png_8(out_file: Path, template: Template) -> None:
    export_png(out_file, template, 8)


@exporter("png-32", ".x32.png", "PNG palette image with size 32px.")
def export_png_8(out_file: Path, template: Template):
    export_png(out_file, template, 32)


@exporter("gpl", ".gpl", "Gimp/Inkscape color palette.")
def export_gimp(out_file: Path, template: Template):
    with out_file.open("w") as file:
        file.write("GIMP Palette\n")
        file.write(f"Name: {template.name}\n")
        file.write(f"Columns: 0\n")

        if template.description:
            file.write(f"# Description: {template.description}\n")
        if template.version:
            file.write(f"# Version: {template.version}\n")
        if template.author:
            file.write(f"# Author: {template.author}\n")
        if template.source:
            file.write(f"# Source: {template.source}\n")

        file.write(f"#")

        for entry in template.colors:
            c = entry.color.as_rgb_tuple()
            file.write(
                f"\n{c[0]:d}\t{c[1]:d}\t{c[2]:d}\t{entry.name}"
            )
            if entry.description:
                file.write(f" - {entry.description}")


@exporter("hex", ".hex", "Simple HEX color palette.")
def export_hex(out_file: Path, template: Template):
    colors: List[str] = []
    for entry in template.colors:
        c = entry.color.as_rgb_tuple()
        colors.append(
            f"{c[0]:02x}{c[1]:02x}{c[2]:02x}"
        )
    with out_file.open("w") as file:
        file.writelines("\n".join(colors))


# @exporter("ase", ".ase", "Color palette for Adobe products (Adobe Swatch Exchange).")
# def export_adobe_swatch_exchange(out_file: Path, template: Template):
#    # https://medium.com/swlh/mastering-adobe-color-file-formats-d29e43fde8eb
#    # http://www.selapa.net/swatches/colors/fileformats.php#adobe_ase
#    with out_file.open("wb") as file:
#        # Write header
#        file.write(b"\x41\x53\x45\x46")  # Signature (Constant: ASEF)
#        file.write(b"\x00\x01\x00\x00")  # Version (Constant: 1.0)
#        file.write(b"\x00\x00\x00\x03")  # Number of blocks
#
#        # Group start
#        file.write(b"\xC0\x01")  # Block type (Group start)
#        file.write(b"\x00\x00\x00\x00")  # Block length
#        file.write(b"\x00\x00")  # Name length
#        file.write(b"\x00")  # 0-terminated group name encoded in UTF-16
#
#        # Color entry
#        file.write(b"\x00\x01")  # Block type (Color entry)
#        file.write(b"\x00\x00\x00\x00")  # Block length
#        file.write(b"\x00\x00")  # Name length
#        file.write(b"\x00")  # 0-terminated color name encoded in UTF-16
#        file.write(b"\x52\x47\x42\x20")  # Color space (Constant: RGB)
#        file.write(b"\x00\x00\x00\x00")  # Red
#        file.write(b"\x00\x00\x00\x00")  # Green
#        file.write(b"\x00\x00\x00\x00")  # Blue
#        file.write(b"\x00\x02")  # Color mode (Constant: Normal)
#
#        # Group end
#        file.write(b"\xC0\x02")  # Block type (Group end)
#        file.write(b"\x00\x00\x00\x00")  # Block length (Constant for Group end)


# @exporter("paintnet", ".txt", "Paint.NET color palette.")
# def export_paint_net(out_file: Path, template: Template):
#    https://www.getpaint.net/doc/latest/WorkingWithPalettes.html
#    ;paint.net Palette File
#    ;Downloaded from Lospec.com/palette-list
#    ;Palette Name: Lospec500
#    ;Description: A collaboration from the Lospec Discord server to create a palette celebrating 500 palettes hosted on Lospec.
#    ;Colors: 42
#    FF10121c
#    FF2c1e31
#    FF6b2643
#    pass


# @exporter("paintshop", ".pal", "Paintshop Pro color palette.")
# def export_jasc(out_file: Path, template: Template):
#    # https://liero.nl/lierohack/docformats/other-jasc.html
#    # JASC-PAL      <- constant string
#    # 0100          <- constant version of palette file format
#    # 16            <- color count
#    # 255 0 0       <- [0-255] rgb separated by space
#    # 0 255 0
#    # 0 0 255
#    # 255 255 0
#    pass


# @exporter("krita", ".kpl", "Krita color palette.")
# def export_krita(out_file: Path, template: Template):
#    # https://docs.krita.org/en/untranslatable_pages/kpl_defintion.html
#    pass


# @exporter("office", ".soc", "Color palette for StarOffice/OpenOffice/LibreOffice.")
# def export_star_office(out_file: Path, template: Template):
#    # http://www.selapa.net/swatches/colors/fileformats.php#ooo_soc
#    pass


# @exporter("scribus", ".xml", "Color palette for Scribus.")
# def export_scribus(out_file: Path, template: Template):
#    # https://github.com/1j01/anypalette.js
#    pass


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
        for file in PALETTES_SOURCE_DIR.glob(TEMPLATE_FILE_PATTERN):
            rel_path: Path = file.relative_to(PALETTES_SOURCE_DIR)
            console.print(rel_path)
            try:
                template: Template = Template.load(file)
                console.print(f"Exporting {template.name}")
                for exporter in EXPORTERS.keys():
                    exporter_info: ExporterInfo = EXPORTERS.get(exporter)
                    export_path: Path = PALETTES_DST_DIR.joinpath(rel_path).with_suffix(exporter_info.suffix)
                    export_path.parent.mkdir(parents=True, exist_ok=True)  # Ensure folders
                    status.update(f"Exporting {exporter} to [i]{export_path}[/i]")
                    exporter_info.fn(export_path, template)
                    console.print(f"Exported to [i]{export_path}[/i]")
            except Exception as e:
                console.print(f"{type(e).__name__}: {str(e)}" if e else "Export failed", style="red")
        console.print("Done")


@app.callback(invoke_without_command=True)
def main(ctx: typer.Context) -> None:
    """
    Color palette tools.
    """
    if ctx.invoked_subcommand is None:
        console.print("Initializing database")
        console.print(Panel("Hello, [red]World!", title="Welcome", subtitle="Thank you"))


if __name__ == "__main__":
    app()
