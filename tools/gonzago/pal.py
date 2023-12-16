import os
from pathlib import Path
from typing import Callable, Iterator, List, NamedTuple, Optional
import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

import yaml
from pydantic import BaseModel
from pydantic_extra_types.color import Color
from gonzago import BASE_DIR_PATH, SOURCE_DIR_PATH

from gonzago.pydantic import Version


PALETTES_SOURCE_DIR: Path = SOURCE_DIR_PATH.joinpath("./palettes").resolve()
PALETTES_DST_DIR: Path = BASE_DIR_PATH.joinpath("palettes").resolve()


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


def find_templates(root: Path) -> Iterator[Path]:
    root = root.resolve()
    if not root.exists():
        raise StopIteration

    if root.is_file():
        if root.match(TEMPLATE_FILE_PATTERN):
            yield root
        raise StopIteration

    for current, dirs, files in os.walk(root):
        for name in dirs:
            if name.startswith("_"):
                dirs.remove(name)
        for name in files:
            if name.endswith(".yml") or name.endswith(".yaml"):
                path: Path = root.joinpath(current, name)
                yield path


def load_template(file: Path) -> Template:
    if not file.match(TEMPLATE_FILE_PATTERN) or not file.is_file():
        raise TypeError("Not a valid template path")
    with file.open() as stream:
        data: dict = yaml.safe_load(stream)
        return Template.model_validate(data)


def load_valid_templates(root: Path) -> Iterator[Template]:
    for file in find_templates(root):
        try:
            template: Template = load_template(file)
            yield template
        except Exception:
            continue


class FormatterInfo(NamedTuple):
    suffix: str
    description: str
    fn: Callable[[Path, Template], None]


FORMATTERS = dict[str, FormatterInfo]()


def formatter(id: str, suffix: str, description: str = "") -> Callable:
    def inner(fn: Callable[[Path, Template], None]) -> Callable[[Path, Template], None]:
        FORMATTERS[id] = FormatterInfo(suffix=suffix, description=description, fn=fn)
        return fn

    return inner


@formatter("png", ".png", "PNG palette image with size 1px.")
def format_png(out_file: Path, template: Template, size: int = 1) -> None:
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


@formatter("png-8", ".x8.png", "PNG palette image with size 8px.")
def format_png_8(out_file: Path, template: Template) -> None:
    format_png(out_file, template, 8)


@formatter("png-32", ".x32.png", "PNG palette image with size 32px.")
def format_png_8(out_file: Path, template: Template):
    format_png(out_file, template, 32)


@formatter("gpl", ".gpl", "Gimp/Inkscape color palette.")
def format_gimp(out_file: Path, template: Template):
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
            file.write(f"\n{c[0]:d}\t{c[1]:d}\t{c[2]:d}\t{entry.name}")
            if entry.description:
                file.write(f" - {entry.description}")


@formatter("hex", ".hex", "Simple HEX color palette.")
def format_hex(out_file: Path, template: Template):
    colors: List[str] = []
    for entry in template.colors:
        c = entry.color.as_rgb_tuple()
        colors.append(f"{c[0]:02x}{c[1]:02x}{c[2]:02x}")
    with out_file.open("w") as file:
        file.writelines("\n".join(colors))


# @formatter("ase", ".ase", "Color palette for Adobe products (Adobe Swatch Exchange).")
# def format_adobe_swatch_exchange(out_file: Path, template: Template):
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


# @formatter("paintnet", ".txt", "Paint.NET color palette.")
# def format_paint_net(out_file: Path, template: Template):
#   # https://www.getpaint.net/doc/latest/WorkingWithPalettes.html
#   with out_file.open("w") as file:
#        file.write(";paint.net Palette File\n")
#        file.write(f";Palette Name: {template.name}\n")
#        if template.description:
#            file.write(f";Description: {template.description}\n")
#        if template.version:
#            file.write(f";Version: {template.version}\n")
#        if template.author:
#            file.write(f";Author: {template.author}\n")
#        if template.source:
#            file.write(f";Source: {template.source}\n")
#        file.write(f";Colors: {len(template.colors)}\n")
#
#        colors: List[str] = []
#        for entry in template.colors:
#            c = entry.color.as_rgb_tuple()
#            colors.append(f"FF{c[0]:02X}{c[1]:02X}{c[2]:02X}")
#        with out_file.open("w") as file:
#            file.writelines("\n".join(colors))


# @formatter("paintshop", ".pal", "Paintshop Pro color palette.")
# def format_jasc(out_file: Path, template: Template):
#    # https://liero.nl/lierohack/docformats/other-jasc.html
#    # JASC-PAL      <- constant string
#    # 0100          <- constant version of palette file format
#    # 16            <- color count
#    # 255 0 0       <- [0-255] rgb separated by space
#    # 0 255 0
#    # 0 0 255
#    # 255 255 0
#    pass


# @formatter("krita", ".kpl", "Krita color palette.")
# def format_krita(out_file: Path, template: Template):
#    # https://docs.krita.org/en/untranslatable_pages/kpl_defintion.html
#    pass


# @formatter("office", ".soc", "Color palette for StarOffice/OpenOffice/LibreOffice.")
# def format_star_office(out_file: Path, template: Template):
#    # http://www.selapa.net/swatches/colors/fileformats.php#ooo_soc
#    pass


# @formatter("scribus", ".xml", "Color palette for Scribus.")
# def format_scribus(out_file: Path, template: Template):
#    # https://github.com/1j01/anypalette.js
#    pass


app = typer.Typer()
console: Console = Console()


@app.command("new")
def new(
    file: Path = "new_palette_template.yaml", name: str = "New Palette Template"
) -> None:
    """
    Create new palette template.
    """
    # if not file.match(TEMPLATE_FILE_PATTERN):
    #    raise TypeError(f"{file} is not a valid template path")

    data: dict = {
        "name": name if name and len(name) > 0 else "New Palette Template",
        "description": "A brand new palette template.",
        "version": Version(1, 0, 0),
        "author": "David Krummenacher and Gonzago Framework contributors",
        "source": "https://github.com/godot-gonzago/gonzago-design",
        "colors": [
            {
                "name": "Black",
                "description": "Black is an achromatic color.",
                "color": Color("black"),
            },
            {
                "name": "White",
                "description": "White is an achromatic color.",
                "color": Color("white"),
            },
        ],
    }

    template: Template = Template.model_validate(data)
    json: dict = Template.model_dump(template, mode="json")

    file.parent.mkdir(parents=True, exist_ok=True)  # Ensure folders
    with file.open("w") as stream:
        yaml.safe_dump(json, stream, sort_keys=False)


@app.command("check")
def check(path: Path = PALETTES_SOURCE_DIR) -> None:
    """
    Validate palette templates.
    """
    pass


@app.command("ls")
def list_templates(dir: Path = PALETTES_SOURCE_DIR) -> None:
    """
    List palette templates.
    """
    if not dir.exists():
        console.print(f"Path [i]{dir}[/i] does not exist!", style="yellow")
        return

    with console.status(f"Searching templates at [i]{dir}[/i]...") as status:
        valid_templates_count: int = 0
        table: Table = Table("Path", "Name", "Description", "Colors")
        for file in find_templates(dir):
            status.update()
            rel_path: str = file.relative_to(dir).as_posix()
            try:
                template: Template = load_template(file)
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


@app.command("formats")
def list_formats():
    """
    List available formats.
    """
    count: int = len(FORMATTERS)
    if count == 0:
        console.print("No exporters available!", style="yellow")
        return
    console.print(f"Available exporters: {count}")
    table: Table = Table("ID", "Suffix", "Description")
    for id, (suffix, description, _) in FORMATTERS.items():
        table.add_row(id, suffix, description)
    console.print(table)


@app.command("publish")
def publish(
    src: Path = PALETTES_SOURCE_DIR,
    dst_dir: Path = PALETTES_DST_DIR,
    formats: list[str] = list(FORMATTERS.keys()),
) -> None:
    """
    Publish palettes in specified formats.
    """
    pass


@app.command("readme")
def build_readme(
    src_dir: Path = PALETTES_SOURCE_DIR,
    dst_dir: Path = PALETTES_DST_DIR
):
    """
    Build readme from all palettes.
    """
    pass


@app.callback(no_args_is_help=True)
def main() -> None:
    """
    Color palette tools.
    """
    pass


if __name__ == "__main__":
    app()
