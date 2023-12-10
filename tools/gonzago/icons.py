import os
import xml.etree.ElementTree as ET
from typing import Iterator, List
from xml.dom import minidom
from pathlib import Path
from xml.dom.expatbuilder import TEXT_NODE

import typer
from scour import scour
from rich.console import Console

from gonzago import BASE_DIR_PATH, SOURCE_DIR_PATH


ICONS_SOURCE_DIR: Path = SOURCE_DIR_PATH.joinpath("./engine/editor_icons").resolve()
ICONS_DST_DIR: Path = BASE_DIR_PATH.joinpath("icons").resolve()


app = typer.Typer()
console: Console = Console()


ICON_FILE_PATTERN: str = "**/*.svg"


_SCOUR_OPTIONS = scour.parse_args(
    [
        "--set-precision=5",
        "--create-groups",
        "--strip-xml-prolog",
        "--remove-descriptive-elements",
        "--enable-comment-stripping",
        "--enable-viewboxing",
        "--no-line-breaks",
        "--strip-xml-space",
        "--enable-id-stripping",
        "--shorten-ids",
        "--quiet",
    ]
)


def optimize_svg(rel_path: Path, scour_options=_SCOUR_OPTIONS) -> None:
    # Sanitize paths
    src_file: Path = ICONS_SOURCE_DIR.joinpath(rel_path).resolve()
    out_file: Path = ICONS_DST_DIR.joinpath(rel_path).resolve()

    # Ensure folders
    out_file.parent.mkdir(parents=True, exist_ok=True)

    # Optimize
    scour_options.infilename = src_file
    scour_options.outfilename = out_file
    (input, output) = scour.getInOut(scour_options)
    scour.start(scour_options, input, output)


def find_icons(root: Path) -> Iterator[Path]:
    root = root.resolve()
    if not root.exists():
        raise StopIteration

    if root.is_file():
        if root.match(ICON_FILE_PATTERN):
            yield root
        raise StopIteration

    for current, dirs, files in os.walk(root):
        for name in dirs:
            if name.startswith("_"):
                dirs.remove(name)
        for name in files:
            if name.endswith(".svg"):
                path: Path = root.joinpath(current, name)
                yield path


# TODO: SVG Meta
# https://docs.python.org/3/library/xml.dom.minidom.html
# https://docs.python.org/3/library/xml.etree.elementtree.html#tutorial
# https://inkscape.org/de/entwickeln/das-svg-format/


def get_meta_data(file: Path) -> dict:
    rel_path: Path = file.relative_to(ICONS_SOURCE_DIR)
    meta: dict = {
        "rel_path": rel_path.as_posix()
    }

    namespaces: dict = {
        # Default SVG namespaces
        # https://www.w3.org/2000/svg
        "": "http://www.w3.org/2000/svg",
        "svg": "http://www.w3.org/2000/svg",
        # Inkscape namespaces
        # https://wiki.inkscape.org/wiki/Inkscape-specific_XML_attributes
        "sodipodi": "http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd",
        "inkscape": "http://www.inkscape.org/namespaces/inkscape",
        # Resource Description Framework
        # https://www.w3.org/TR/1999/REC-rdf-syntax-19990222/
        "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
        # Dublin Core Metadata Initiative
        # https://www.dublincore.org/specifications/dublin-core/dcmi-terms/
        "dc": "http://purl.org/dc/elements/1.1/",
        # Creative Commons Rights Expression Language
        # https://creativecommons.org/ns
        "cc": "http://creativecommons.org/ns#"
    }

    tree: ET.ElementTree = ET.parse(file)

    svg: ET.Element = tree.getroot()
    if "width" in svg.keys():
        meta["width"] = int(svg.get("width"))
    if "height" in svg.keys():
        meta["height"] = int(svg.get("height"))
    if "viewBox" in svg.keys():
        vb: str = svg.get("viewBox")
        vb_split: list[str] = vb.split(" ")
        meta["view_box"] = (
            int(vb_split[0]),
            int(vb_split[1]),
            int(vb_split[2]),
            int(vb_split[3])
        )
    if "version" in svg.keys():
        meta["version"] = svg.get("version")

    metadata: ET.Element = svg.find("metadata", namespaces)
    if metadata is None:
        title: str = svg.findtext("title", namespaces=namespaces)
        if title:
            meta["title"] = title
        return meta

    # Dublin Core Metadata (dc:format, dc:type are not present in Inkscape)
    meta["title"] = metadata.findtext("rdf:RDF/cc:Work/dc:title", namespaces=namespaces)
    meta["description"] = metadata.findtext("rdf:RDF/cc:Work/dc:description", namespaces=namespaces)

    meta["identifier"] = metadata.findtext("rdf:RDF/cc:Work/dc:identifier", namespaces=namespaces)
    subject: list[str] = []
    for element in metadata.findall("rdf:RDF/cc:Work/dc:subject/rdf:Bag/rdf:li", namespaces):
        subject.append(element.text)
    meta["subject"] = subject

    meta["date"] = metadata.findtext("rdf:RDF/cc:Work/dc:date", namespaces=namespaces)
    meta["source"] = metadata.findtext("rdf:RDF/cc:Work/dc:source", namespaces=namespaces)
    meta["relation"] = metadata.findtext("rdf:RDF/cc:Work/dc:relation", namespaces=namespaces)
    meta["language"] = metadata.findtext("rdf:RDF/cc:Work/dc:language", namespaces=namespaces)

    meta["creator"] = metadata.findtext("rdf:RDF/cc:Work/dc:creator/cc:Agent/dc:title", namespaces=namespaces)
    meta["contributor"] = metadata.findtext("rdf:RDF/cc:Work/dc:contributor/cc:Agent/dc:title", namespaces=namespaces)
    meta["publisher"] = metadata.findtext("rdf:RDF/cc:Work/dc:publisher/cc:Agent/dc:title", namespaces=namespaces)
    meta["rights"] = metadata.findtext("rdf:RDF/cc:Work/dc:rights/cc:Agent/dc:title", namespaces=namespaces)
    meta["coverage"] = metadata.findtext("rdf:RDF/cc:Work/dc:coverage", namespaces=namespaces)
    license: ET.Element = metadata.find("rdf:RDF/cc:Work/cc:license", namespaces)
    if not license is None:
        if "{http://www.w3.org/1999/02/22-rdf-syntax-ns#}resource" in license.keys():
            meta["license"] = license.get("{http://www.w3.org/1999/02/22-rdf-syntax-ns#}resource")

    return meta


# TODO: Markdown
# https://medium.com/analytics-vidhya/7-advanced-markdown-tips-5a031620bf52
# https://docs.github.com/de/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax
# https://github.com/DavidWells/advanced-markdown
# https://github.com/markdown-templates/markdown-snippets
# https://www.markdownguide.org/extended-syntax/
# https://github.github.com/gfm/
# https://github.github.com/gfm/#html-blocks
# https://gist.github.com/seanh/13a93686bf4c2cb16e658b3cf96807f2


@app.command("meta")
def test_meta_data():
    path: Path = ICONS_SOURCE_DIR.joinpath("camera/camera.svg").resolve()
    #print(path.read_text())
    meta: dict = get_meta_data(path)
    print(meta)

@app.command("build")
def build():
    """
    Build optimized icons.
    """

    console.print(f"Building icons...")
    with console.status("Building templates...") as status:
        for file in find_icons(ICONS_SOURCE_DIR):
            rel_path: Path = file.relative_to(ICONS_SOURCE_DIR)
            console.print(f"Exporting {rel_path}")
            optimize_svg(rel_path)
            status.update(f"Exporting [i]{file}[/i]")
        console.print("Done")


@app.callback(no_args_is_help=True)
def main() -> None:
    """
    Editor icon tools.
    """


if __name__ == "__main__":
    app()
