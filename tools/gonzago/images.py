from pathlib import Path

import typer
from scour import scour
from typing_extensions import Annotated


app = typer.Typer()


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


def _minimize_svg(src_file: Path, out_file: Path, scour_options=_SCOUR_OPTIONS) -> None:
    # Sanitize paths
    src_file: Path = src_file.resolve(True)
    out_file: Path = out_file.with_suffix(".svg").resolve()

    # Ensure folders
    out_file.parent.mkdir(parents=True, exist_ok=True)

    # Optimize
    scour_options.infilename = src_file
    scour_options.outfilename = out_file
    (input, output) = scour.getInOut(scour_options)
    scour.start(scour_options, input, output)

@app.command()
def optimize_icons(
    src_dir: Annotated[
        Path,
        typer.Option(
            exists=True,
            dir_okay=True,
            readable=True,
            resolve_path=True,
        ),
    ],
    out_dir: Annotated[
        Path,
        typer.Option(
            dir_okay=True,
            writable=True,
            resolve_path=True,
        ),
    ],
    scour_options=_SCOUR_OPTIONS,
) -> None:
    for src_file in src_dir.rglob("*.svg"):
        rel_path: Path = src_file.relative_to(src_dir)
        out_file: Path = out_dir.joinpath(rel_path)
        print("Exporting {}...".format(rel_path.as_posix()))
        _minimize_svg(src_file, out_file, scour_options)


# https://wiki.inkscape.org/wiki/Using_the_Command_Line
# https://inkscape.org/doc/inkscape-man.html
@app.command()
def inkscape_to_png(
    src_file: Annotated[
        Path,
        typer.Option(
            exists=True,
            file_okay=True,
            readable=True,
            resolve_path=True,
        ),
    ],
    out_file: Annotated[
        Path,
        typer.Option(
            file_okay=True,
            writable=True,
            resolve_path=True,
        ),
    ],
) -> None:
    import subprocess

    # shutil.which
    # https://docs.python.org/3/library/subprocess.html#subprocess.Popen
    # https://docs.python.org/3/library/subprocess.html#subprocess.run

    inkscape: Path = Path("C:/Program Files/Inkscape/bin/inkscape.exe").resolve()
    blender: Path = Path(
        "C:/Program Files/Blender Foundation/Blender 3.4/blender.exe"
    ).resolve()

    # Sanitize paths
    src_file: Path = src_file.resolve(True)
    out_file: Path = out_file.with_suffix(".png").resolve()

    # Ensure folders
    out_file.parent.mkdir(parents=True, exist_ok=True)

    # Convert
    # inkscape --export-filename=out_file.png src_file.svg
    subprocess.run([inkscape, "--export-filename", out_file, src_file])
    pass


@app.command()
def svg_to_png(
    src_file: Annotated[
        Path,
        typer.Option(
            exists=True,
            file_okay=True,
            readable=True,
            resolve_path=True,
        ),
    ],
    out_file: Annotated[
        Path,
        typer.Option(
            file_okay=True,
            writable=True,
            resolve_path=True,
        ),
    ],
) -> None:
    # Sanitize paths
    src_file: Path = src_file.resolve(True)
    out_file: Path = out_file.with_suffix(".png").resolve()

    # Ensure folders
    out_file.parent.mkdir(parents=True, exist_ok=True)

    # Convert (https://cairosvg.org/documentation/)
    #from cairosvg import svg2png

    #svg2png(url=str(src_file), write_to=str(out_file))


# @app.command()
def build_os_icons(src_files: set[Path], out_dir: Path) -> None:
    import xml.etree.ElementTree as ET

    # ICO
    # https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html#ico
    # https://docs.godotengine.org/en/stable/tutorials/export/changing_application_icon_for_windows.html
    # https://en.wikipedia.org/wiki/ICO_(file_format)
    # https://www.geeksforgeeks.org/convert-png-to-ico-with-pillow-in-python/
    # https://learning-python.com/iconify.html
    # https://github.com/python-pillow/Pillow/pull/6122
    # 16×16,    24x24, 32×32,    48×48, 64×64, 128×128,    256×256
    # ICNS
    # https://docs.fileformat.com/image/icns/
    # https://en.wikipedia.org/wiki/Apple_Icon_Image_format
    # https://pypi.org/project/icnsutil/
    # https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html#icns
    # 16×16,           32×32,    48×48,        128×128,    256×256,    512x512,
    # 16x16@2x,        32x32@2x,               128x128@2x, 256x256@2x, 512x512@2x
    # TODO: Check sizes of source files
    src_file_size_dict: dict = dict()
    for src_file in src_files:
        if src_file.suffix != ".svg":
            continue
        src_file = src_file.resolve(True)
        tree = ET.parse(src_file)
        root = tree.getroot()
        src_file_size: int = max(
            int(root.attrib.get("width", "0")), int(root.attrib.get("height", "0"))
        )
        if src_file_size == 0:
            continue
        src_file_size_dict[src_file_size] = src_file

    # TODO: Temporary folder export pngs, get source files based on requested size >= source size
    src_file_size_list: list[int] = sorted(src_file_size_dict.keys(), reverse=True)

    print(src_file_size_dict)
    print(src_file_size_list)

    # 16×16 + @2x
    # 24x24
    # 32×32 + @2x
    # 48×48
    # 64×64
    # 128×128 + @2x
    # 256×256 + @2x
    # 512x512 + @2x

    target_sizes: list[int] = [16, 24, 32, 48, 64, 128, 256, 512]
    target_scales: list[int] = [16, 32, 128, 256, 512]

    src_file_size: int = -1
    for target_size in target_sizes:
        # Find source files based on requested size >= source size
        for src_file_size_entry in src_file_size_list:
            if (
                src_file_size_entry <= target_size
                and src_file_size_entry > src_file_size
            ):
                src_file_size = src_file_size_entry

        print(
            f"target_size:{target_size} -> src_size:{src_file_size}, plus scaling: {target_size in target_scales} -> {src_file_size_dict[src_file_size]}"
        )

    # MOBILE?

    # Ensure folders
    # out_dir = out_dir.resolve()
    # out_dir.mkdir(parents=True, exist_ok=True)
    pass


@app.command()
def build_splash_image() -> None:
    pass


@app.callback(no_args_is_help=True)
def main() -> None:
    """
    Editor images tools.
    """


if __name__ == "__main__":
    app()
