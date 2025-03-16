import typer

from .create import create
from .import_palette import import_palette
from .list_palettes import list_palettes
from .list_readers import list_readers
from .list_writers import list_writers
from .publish import publish

palettes = typer.Typer(
    name="palettes", help="Color palette tools.", no_args_is_help=True
)

palettes.command("create")(create)
palettes.command("import")(import_palette)
palettes.command("list")(list_palettes)
palettes.command("readers")(list_readers)
palettes.command("writers")(list_writers)
palettes.command("publish")(publish)


@palettes.callback(no_args_is_help=True)
def main() -> None:
    """
    Color palette tools.
    """
    pass
