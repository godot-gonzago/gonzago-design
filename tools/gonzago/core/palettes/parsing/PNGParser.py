from pathlib import Path

from PIL import Image, ImageDraw
from PIL.PngImagePlugin import PngInfo
from pydantic import PositiveInt

from ..models import Palette
from . import PaletteReader, PaletteWriter


class PNGPaletteReader(PaletteReader):
    def read(self, file: Path) -> Palette:
        raise NotImplementedError()

    def validate(self, file: Path) -> bool:
        raise NotImplementedError()


class PNGPaletteWriter(PaletteWriter):
    size: PositiveInt = 1

    def write(self, palette: Palette, file: Path) -> None:
        """
        PNG

        PNG palette image.
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
        image: Image = Image.new("RGB", (color_count * self.size, self.size))

        draw = ImageDraw.Draw(image, "RGB")
        for i in range(color_count):
            color = palette.colors[i].color
            draw.rectangle(
                (i * self.size, 0, i * self.size + self.size, self.size),
                color.as_rgb_tuple(
                    alpha=False
                ),  # TODO: Alpha handling doesn't seems to work here
            )

        # Test here https://www.metadata2go.com/view-metadata
        info: PngInfo = PngInfo()
        metadata: dict = palette.model_dump(
            exclude=["colors"], mode="json", exclude_defaults=True
        )
        for key, value in metadata.items():
            info.add_text(f"dcm_{key}", str(value))
        info.add_text("dcm_scale", str(self.size))

        image.save(file, "PNG", pnginfo=info)


PaletteReader._register_reader(
    PNGPaletteReader(id="png", description="PNG palette image.", pattern="*.png")
)
PaletteWriter._register_writer(
    PNGPaletteWriter(
        id="png", description="PNG palette image with size 1px.", suffix=".png"
    )
)
PaletteWriter._register_writer(
    PNGPaletteWriter(
        id="png-8",
        description="PNG palette image with size 8px.",
        suffix=".x8.png",
        size=8,
    )
)
PaletteWriter._register_writer(
    PNGPaletteWriter(
        id="png-32",
        description="PNG palette image with size 32px.",
        suffix=".x32.png",
        size=32,
    )
)
