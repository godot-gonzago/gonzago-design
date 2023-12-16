from pathlib import Path
from typing import Callable, List, NamedTuple

from .templates import Template


class ExporterInfo(NamedTuple):
    suffix: str
    description: str
    fn: Callable[[Path, Template], None]


EXPORTERS = dict[str, ExporterInfo]()


# TODO: Allow for parameters, so we can only have one method with
#       multiple decorators.
# *args, **kwargs
# https://docs.python.org/3/library/typing.html#annotating-callable-objects
# https://docs.python.org/3/library/typing.html#typing.ParamSpec
# https://docs.python.org/3/library/typing.html#typing.Concatenate
# https://sobolevn.me/2021/12/paramspec-guide


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
            file.write(f"\n{c[0]:d}\t{c[1]:d}\t{c[2]:d}\t{entry.name}")
            if entry.description:
                file.write(f" - {entry.description}")


@exporter("hex", ".hex", "Simple HEX color palette.")
def export_hex(out_file: Path, template: Template):
    colors: List[str] = []
    for entry in template.colors:
        c = entry.color.as_rgb_tuple()
        colors.append(f"{c[0]:02x}{c[1]:02x}{c[2]:02x}")
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


#@exporter("paintnet", ".txt", "Paint.NET color palette.")
#def export_paint_net(out_file: Path, template: Template):
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
