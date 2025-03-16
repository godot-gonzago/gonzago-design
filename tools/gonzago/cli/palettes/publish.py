from pathlib import Path

from jinja2 import Environment, FileSystemLoader, Template
from rich.console import Console

from gonzago.core.config import CONFIG
from gonzago.core.palettes.io import get_palette_files
from gonzago.core.palettes.models import Palette
from gonzago.core.palettes.parsing import PaletteWriter

PALETTES_SOURCE_DIR: Path = CONFIG.src_path("./palettes")
PALETTES_DST_DIR: Path = CONFIG.dst_path("palettes")


console: Console = Console()


# TODO: https://typer.tiangolo.com/tutorial/progressbar/#spinner
# TODO: https://typer.tiangolo.com/tutorial/progressbar/#progress-bar_1
# TODO: https://rich.readthedocs.io/en/stable/progress.html#basic-usage
def publish() -> None:
    """
    Publish palettes in full.
    """

    console.print("Gathering export formats")
    formats: list[PaletteWriter] = list(PaletteWriter.get_writers())

    console.print("Gathering palettes")
    palettes: list[Palette] = list()
    for file in get_palette_files(PALETTES_SOURCE_DIR):
        console.print(f"Reading [i]'{file.as_posix()}'[/i]...")
        palette: Palette
        try:
            palette = file.read()
            palettes.append(palette)
        except Exception as e:
            console.print(e, style="red")
            continue

        console.print(f"Exporting [i]'{file.as_posix()}'[/i]...")
        for format in formats:
            try:
                file_out = file.create_output_file(PALETTES_DST_DIR, format)
                file_out.write()
                console.print(f"Exported [i]'{file_out.as_posix()}'[/i]")
            except Exception as e:
                console.print(e, style="red")
                continue

    console.status("Building [i]'README.md'[/i]...")

    environment: Environment = Environment(loader=FileSystemLoader(PALETTES_SOURCE_DIR))
    environment.trim_blocks = True
    environment.lstrip_blocks = True
    template: Template = environment.get_template("README.md.jinja")
    content: str = template.render(formats=formats, palettes=palettes)

    console.status("Writing [i]'README.md'[/i]...")
    path: Path = PALETTES_DST_DIR.joinpath("README.md").resolve()
    path.write_text(content)

    console.print("Done")


# TODO: COPYRIGHT.txt https://www.debian.org/doc/packaging-manuals/copyright-format/1.0/
# CHANGELOG.md
# CONTRIBUTING.md
# AUTHORS.md
# SUPPORT.md
# ACKNOWLEDGMENTS.md
# https://github.com/kmindi/special-files-in-repository-root/blob/master/README.md
