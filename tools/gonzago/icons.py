from typing import List
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


@app.command("build")
def build():
    """
    Build optimized icons.
    """

    console.print(f"Building icons...")
    with console.status("Building templates...") as status:
        for file in ICONS_SOURCE_DIR.glob(ICON_FILE_PATTERN):
            rel_path: Path = file.relative_to(ICONS_SOURCE_DIR)
            console.print(f"Exporting {rel_path}")

            with file.open() as stream:
                doc: minidom.Document = minidom.parse(stream)
                svg_nodes = doc.getElementsByTagName("svg")
                if len(svg_nodes) > 0:
                    svg_root: minidom.Element = svg_nodes[0]
                    if svg_root.hasAttribute("width"):
                        print(svg_root.getAttribute("width"))
                    if svg_root.hasAttribute("height"):
                        print(svg_root.getAttribute("height"))
                    title_nodes = svg_root.getElementsByTagName("title")
                    if len(title_nodes) > 0:
                        title_element: minidom.Element = title_nodes[0]
                        if title_element and title_element.hasChildNodes():
                            print(title_element.childNodes[0].nodeValue)
                    meta_data_nodes = svg_root.getElementsByTagName("metadata")
                    if len(meta_data_nodes) > 0:
                        meta_data_element: minidom.Element = meta_data_nodes[0]
                        if meta_data_element:
                            print("has_meta_data")

            optimize_svg(rel_path)
            status.update(f"Exporting [i]{file}[/i]")
        console.print("Done")



# <?xml version="1.0" encoding="UTF-8" standalone="no"?>
# <!-- Created with Inkscape (http://www.inkscape.org/) -->
#
# <svg
#    width="16"
#    height="16"
#    viewBox="0 0 16 16"
#    version="1.1"
#    id="godot_editor_icon"
#    inkscape:version="1.3 (0e150ed6c4, 2023-07-21)"
#    sodipodi:docname="gonzago.svg"
#    xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape"
#    xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd"
#    xmlns="http://www.w3.org/2000/svg"
#    xmlns:svg="http://www.w3.org/2000/svg"
#    xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
#    xmlns:cc="http://creativecommons.org/ns#"
#    xmlns:dc="http://purl.org/dc/elements/1.1/">
#   <title
#      id="title">Gonzago Framework Editor Icon</title>
#   <metadata
#      id="metadata">
#     <rdf:RDF>
#       <cc:Work
#          rdf:about="">
#         <dc:title>Gonzago Framework Editor Icon</dc:title>
#         <dc:creator>
#           <cc:Agent>
#             <dc:title>David Krummenacher</dc:title>
#           </cc:Agent>
#         </dc:creator>
#         <dc:source>https://github.com/godot-gonzago</dc:source>
#         <dc:publisher>
#           <cc:Agent>
#             <dc:title>Gonzago Framework</dc:title>
#           </cc:Agent>
#         </dc:publisher>
#         <dc:subject>
#           <rdf:Bag>
#             <rdf:li>editor</rdf:li>
#             <rdf:li>icon</rdf:li>
#             <rdf:li>gonzago</rdf:li>
#           </rdf:Bag>
#         </dc:subject>
#         <dc:language>en</dc:language>
#         <dc:identifier>gonzago.editor_icons.gonzago</dc:identifier>
#         <dc:date>2023-11-19</dc:date>
#         <dc:rights>
#           <cc:Agent>
#             <dc:title>Copyright (c) 2023 David Krummenacher and Gonzago Framework contributors</dc:title>
#           </cc:Agent>
#         </dc:rights>
#         <cc:license
#            rdf:resource="http://creativecommons.org/licenses/by/4.0/" />
#         <dc:description>A skull with a crown in reference to The Murder of Gonzago, a play within The Tragedy of Hamlet, Prince of Denmark.</dc:description>
#         <dc:contributor>
#           <cc:Agent>
#             <dc:title>David Krummenacher</dc:title>
#           </cc:Agent>
#         </dc:contributor>
#       </cc:Work>
#       <cc:License
#          rdf:about="http://creativecommons.org/licenses/by/4.0/">
#         <cc:permits
#            rdf:resource="http://creativecommons.org/ns#Reproduction" />
#         <cc:permits
#            rdf:resource="http://creativecommons.org/ns#Distribution" />
#         <cc:requires
#            rdf:resource="http://creativecommons.org/ns#Notice" />
#         <cc:requires
#            rdf:resource="http://creativecommons.org/ns#Attribution" />
#         <cc:permits
#            rdf:resource="http://creativecommons.org/ns#DerivativeWorks" />
#       </cc:License>
#     </rdf:RDF>
#   </metadata>
#   <sodipodi:namedview
#      id="base_view"
#      pagecolor="#333b4f"
#      bordercolor="#8f939e"
#      borderopacity="1"
#      inkscape:pageshadow="0"
#      inkscape:pageopacity="0"
#      inkscape:pagecheckerboard="false"
#      inkscape:document-units="px"
#      showgrid="true"
#      units="px"
#      width="16px"
#      viewbox-height="16"
#      inkscape:zoom="22.627417"
#      inkscape:cx="8.5515726"
#      inkscape:cy="10.429825"
#      inkscape:window-width="1368"
#      inkscape:window-height="850"
#      inkscape:window-x="-6"
#      inkscape:window-y="-6"
#      inkscape:window-maximized="1"
#      inkscape:current-layer="base_layer"
#      showborder="true"
#      inkscape:snap-grids="true"
#      inkscape:showpageshadow="0"
#      inkscape:deskcolor="#1c202b">
#     <inkscape:grid
#        type="xygrid"
#        id="base_grid"
#        dotted="true"
#        empspacing="4"
#        originx="0"
#        originy="0"
#        spacingy="1"
#        spacingx="1"
#        units="px"
#        visible="true"
#        color="#699ce8"
#        opacity="0.29803922"
#        empcolor="#699ce8"
#        empopacity="0.29803922" />
#   </sodipodi:namedview>
#   <defs
#      id="base_definitions" />
#   <g
#      inkscape:label="Base Layer"
#      inkscape:groupmode="layer"
#      id="base_layer">
#     <path
#        id="gonzago"
#        d="M 8,1.4 5,4 2,2.2 V 7 H 14 V 2.2 L 11,4 Z M 2,8 v 2 c 0,1.3 0.8,2.4 2,2.8 V 14 c 0,0.6 0.4,1 1,1 h 6 c 0.6,0 1,-0.4 1,-1 v -1.2 c 1.2,-0.4 2,-1.5 2,-2.8 V 8 Z m 1.2,2 h 4 c 0,1.1 -0.9,2 -2,2 -1.1,0 -2,-0.9 -2,-2 z m 5.6,0 h 4 c 0,1.1 -0.9,2 -2,2 -1.1,0 -2,-0.9 -2,-2 z M 8,11 9,13 H 7 Z"
#        fill="#e0e0e0" />
#   </g>
# </svg>




@app.callback(no_args_is_help=True)
def main() -> None:
    """
    Editor icon tools.
    """


if __name__ == "__main__":
    app()
