from pathlib import Path

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
