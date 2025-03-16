import os
import string
from fnmatch import fnmatch
from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console

from gonzago.core.config import CONFIG
from gonzago.core.icons.io import find_icons, get_meta_data, optimize_svg

ICONS_SOURCE_DIR: Path = CONFIG.src_path("./engine/editor_icons")
ICONS_DST_DIR: Path = CONFIG.dst_path("icons")


app = typer.Typer()
console: Console = Console()


@app.command("meta")
def print_meta_data(
    path: Annotated[
        Path,
        typer.Argument(
            help="The file path of the icon. Can be relative to source directory"
        ),
    ],
):
    """
    Print meta data for icon file at path.
    """

    if not path.is_absolute():
        path = ICONS_SOURCE_DIR.joinpath(path).resolve()
    meta: dict = get_meta_data(path)
    console.print(meta)


@app.command("publish")
def publish():
    """
    Build optimized icons.
    """

    console.print("Building icons...")
    with console.status("Building templates...") as status:
        for file in find_icons(ICONS_SOURCE_DIR):
            rel_path: Path = file.relative_to(ICONS_SOURCE_DIR)
            console.print(f"Exporting {rel_path}")
            optimize_svg(rel_path)
            status.update(f"Exporting [i]{file}[/i]")
        console.print("Done")


@app.command("alt_readme")
def _read_me():
    ICONS_PER_ROW: int = 2
    COLUMNS_PER_ICON: int = 2

    lines: list[str] = [
        "# Gonzago Framework Editor Icons",
        "",
        "Editor icons for use in Gonzago Framework",
        "",
        "## Icons",
        "<table>",
    ]

    for current, dirs, files in os.walk(ICONS_SOURCE_DIR):
        for name in dirs:
            if not fnmatch(name, "[!._]*"):
                dirs.remove(name)

        file_paths: list[Path] = []
        for name in files:
            if fnmatch(name, "*.svg"):
                file_path: Path = Path(current, name)
                file_paths.append(file_path)

        files_count: int = len(file_paths)
        if files_count > 0:
            folder_path: Path = ICONS_SOURCE_DIR.joinpath(current)
            folder_rel_path: Path = folder_path.relative_to(ICONS_SOURCE_DIR)
            folder_name: str = (
                string.capwords(folder_rel_path.as_posix().replace("/", "."), ".")
                if folder_rel_path.name
                else "Gonzago"
            )
            lines.extend(
                [
                    f'  <thead><tr><th align="left" colspan="{str(ICONS_PER_ROW * COLUMNS_PER_ICON)}" width="2048">{folder_name}</th></tr></thead>',
                    "  <tbody>",
                ]
            )

            for row_start_idx in range(0, files_count, ICONS_PER_ROW):
                row_end_idx: int = row_start_idx + ICONS_PER_ROW
                lines.append("    <tr>")

                for icon_idx in range(row_start_idx, min(row_end_idx, files_count)):
                    full_path: Path = ICONS_SOURCE_DIR.joinpath(
                        file_paths[icon_idx]
                    ).resolve()
                    rel_path: Path = full_path.relative_to(ICONS_SOURCE_DIR)
                    meta: dict[str] = get_meta_data(full_path)

                    lines.extend(
                        [
                            f'      <td><img src="{Path("/icons").joinpath(rel_path).as_posix()}" width="24" height="24"></td>',
                            "      <td>",
                            "        <p>",
                            f"          {meta.get('title', rel_path.stem)}",
                        ]
                    )
                    relation: str = meta.get("relation")
                    if relation:
                        lines.append(
                            f'          <a href="{relation}" target="_blank">:pushpin:</a>'
                        )
                    subject: list[str] = meta["subject"]
                    if subject:
                        if "editor" in subject:
                            subject.remove("editor")
                        if "icon" in subject:
                            subject.remove("icon")
                        if len(subject) > 0:
                            lines.append(
                                f"          <br><var>{', '.join(subject)}</var>"
                            )
                    lines.extend(["        </p>", "      </td>"])

                for _ in range(max(row_start_idx, files_count), row_end_idx):
                    lines.append(f'      <td colspan="{str(COLUMNS_PER_ICON)}"></td>')

                lines.append("    </tr>")

            lines.append("  </tbody>")

    lines.extend(["</table>", ""])

    readme_path: Path = ICONS_DST_DIR.joinpath("README.md").resolve()
    with readme_path.open("w") as readme_file:
        readme_file.writelines("\n".join(lines))


@app.command("readme")
def build_readme():
    console.print("Building readme...")
    with console.status("Building readme...") as status:
        path: Path = ICONS_DST_DIR.joinpath("README.md").resolve()
        with path.open("w") as readme:
            readme.write(
                "# Gonzago Framework Editor Icons\n\n"
                "Editor icons for use in Gonzago Framework\n\n"
                "## Icons\n\n"
            )

            folder: Path = Path(".")
            readme.write(
                "<table>\n"
                '<thead><tr><th align="left" colspan="4" width="2048">Gonzago</th></tr></thead>\n'
                "<tbody>\n"
            )
            files_in_row: int = 0
            for file in find_icons(ICONS_SOURCE_DIR):
                rel_path: Path = file.relative_to(ICONS_SOURCE_DIR)
                new_folder: Path = rel_path.parent

                if folder != new_folder:
                    if files_in_row == 1:
                        readme.write('    <td colspan="2"></td>\n  </tr>\n')
                        files_in_row = 0
                    header: str = string.capwords(
                        new_folder.as_posix().replace("/", "."), "."
                    )
                    readme.write(
                        "</tbody>\n"
                        f'<thead><tr><th align="left" colspan="4">{header}</th></tr></thead>\n'
                        "<tbody>\n"
                    )
                    folder = new_folder

                console.print(f"Getting meta {rel_path}")
                image_src: str = Path("/icons").joinpath(rel_path).as_posix()
                meta: dict[str] = get_meta_data(file)
                status.update(f"Writing readme entry for [i]{file}[/i]")

                if files_in_row == 0:
                    readme.write("  <tr>\n")

                readme.write(
                    f'    <td><img src="{image_src}" width="24" height="24"></td>\n'
                    f"    <td><p>{meta.get('title', rel_path.stem)}"
                )
                relation: str = meta.get("relation")
                if relation:
                    readme.write(f' <a href="{relation}" target="_blank">:pushpin:</a>')
                subject: list[str] = meta["subject"]
                if subject:
                    if "editor" in subject:
                        subject.remove("editor")
                    if "icon" in subject:
                        subject.remove("icon")
                    if len(subject) > 0:
                        readme.write(f"<br><var>{', '.join(subject)}</var>")
                readme.write("</p></td>\n")

                if files_in_row == 1:
                    readme.write("  </tr>\n")

                files_in_row += 1
                if files_in_row > 1:
                    files_in_row = 0

            if files_in_row == 1:
                readme.write('    <td colspan="2"></td>\n  </tr>\n')
            readme.write("</tbody>\n</table>\n\n")

        console.print("Done")


# TODO: COPYRIGHT.txt https://www.debian.org/doc/packaging-manuals/copyright-format/1.0/
# CHANGELOG.md
# CONTRIBUTING.md
# AUTHORS.md
# SUPPORT.md
# ACKNOWLEDGMENTS.md
# https://github.com/kmindi/special-files-in-repository-root/blob/master/README.md


@app.callback(no_args_is_help=True)
def main() -> None:
    """
    Editor icon tools.
    """


if __name__ == "__main__":
    app()
