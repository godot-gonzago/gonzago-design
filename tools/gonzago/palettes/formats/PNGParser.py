from pathlib import Path

from PIL import Image, ImageDraw
from PIL.PngImagePlugin import PngInfo

from ..core import Palette
from ..io import register_reader, register_writer


def read(file: Path) -> Palette:
    raise NotImplementedError()


def write(id: str, file: Path, palette: Palette, scale: int = 1) -> None:
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

    # Dublin Core Metadata https://www.dublincore.org/specifications/dublin-core/dcmi-terms/#section-3
    # meta["title"] = metadata.findtext("rdf:RDF/cc:Work/dc:title", namespaces=namespaces)
    # meta["description"] = metadata.findtext("rdf:RDF/cc:Work/dc:description", namespaces=namespaces)
    # meta["identifier"] = metadata.findtext("rdf:RDF/cc:Work/dc:identifier", namespaces=namespaces)
    # meta["subject"] = subject
    # meta["date"] = metadata.findtext("rdf:RDF/cc:Work/dc:date", namespaces=namespaces)
    # meta["source"] = metadata.findtext("rdf:RDF/cc:Work/dc:source", namespaces=namespaces)
    # meta["relation"] = metadata.findtext("rdf:RDF/cc:Work/dc:relation", namespaces=namespaces)
    # meta["language"] = metadata.findtext("rdf:RDF/cc:Work/dc:language", namespaces=namespaces)
    # meta["creator"] = metadata.findtext("rdf:RDF/cc:Work/dc:creator/cc:Agent/dc:title", namespaces=namespaces)
    # meta["contributor"] = metadata.findtext("rdf:RDF/cc:Work/dc:contributor/cc:Agent/dc:title", namespaces=namespaces)
    # meta["publisher"] = metadata.findtext("rdf:RDF/cc:Work/dc:publisher/cc:Agent/dc:title", namespaces=namespaces)
    # meta["rights"] = metadata.findtext("rdf:RDF/cc:Work/dc:rights/cc:Agent/dc:title", namespaces=namespaces)
    # meta["coverage"] = metadata.findtext("rdf:RDF/cc:Work/dc:coverage", namespaces=namespaces)
    # meta["license"] = license.get("{http://www.w3.org/1999/02/22-rdf-syntax-ns#}resource")

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
        info.add_text(
            "source", palette.source
        )  # This might not work, might need better ids

    # Maybe add color info?
    info.add_text("scale", str(scale))

    image.save(file, "PNG", pnginfo=info)


def write_8(id: str, file: Path, palette: Palette) -> None:
    write(id, file, palette, 8)


def write_32(id: str, file: Path, palette: Palette) -> None:
    write(id, file, palette, 32)


register_reader("png", "*.png", "PNG palette image.", read)
register_writer("png", ".png", "PNG palette image with size 1px.", write)
register_writer("png-8", ".x8.png", "PNG palette image with size 8px.", write_8)
register_writer("png-32", ".x32.png", "PNG palette image with size 32px.", write_32)
