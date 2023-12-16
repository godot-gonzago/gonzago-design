from pathlib import Path
from PIL import Image, ImageDraw
from PIL.PngImagePlugin import PngInfo
from ..io import Palette, register_reader, register_writer


ID: str = "png"
PATTERN: str = "*.png"
SUFFIX: str = ".png"
DESCRIPTION = "PNG palette image."


def read(file: Path) -> Palette:
    raise NotImplementedError()


def write(id: str, file: Path, palette: Palette) -> None:
    """
    PNG

    PNG palette image with size 1px.
    """

    # https://dev.exiv2.org/projects/exiv2/wiki/The_Metadata_in_PNG_files
    # https://en.wikipedia.org/wiki/PNG#Ancillary_chunks
    # http://ftp-osl.osuosl.org/pub/libpng/documents/pngext-1.5.0.html#C.eXIf
    # https://docs.gimp.org/2.10/en/plug-in-metadata-editor.html
    # https://gist.github.com/jpstroop/58a21d02370c8ba34dc8f0fdd4206d70
    # https://github.com/python-pillow/Pillow/blob/main/src/PIL/ExifTags.py
    # https://www.iptc.org/standards/photo-metadata/iptc-standard/
    # https://docs.gimp.org/en/plug-in-metadata-viewer.html

    scale: int = 1
    color_count: int = len(palette.colors)
    image: Image = Image.new("RGB", (color_count * scale, scale))

    draw = ImageDraw.Draw(image, "RGB")
    for i in range(color_count):
        color = palette.colors[i].color
        draw.rectangle((i * scale, 0, i * scale + scale, scale), color.as_rgb_tuple())

    # Test here https://www.metadata2go.com/view-metadata
    info: PngInfo = PngInfo()
    info.add_text("name", palette.name)
    if palette.description:
        info.add_text("description", palette.description)
    if palette.version:
        info.add_text("version", str(palette.version))
    if palette.author:
        info.add_text("author", palette.author)
    if palette.source:
        info.add_text("source", palette.source) # This might not work, might need better ids

    # Maybe add color info?
    info.add_text("scale", str(scale))

    image.save(file, "PNG", pnginfo=info)


register_reader(ID, PATTERN, DESCRIPTION, read)
register_writer(ID, SUFFIX, DESCRIPTION, write)
