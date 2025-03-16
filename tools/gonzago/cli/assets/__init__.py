import typer

from .publish import publish

assets_app = typer.Typer()

assets_app.command("publish")(publish)


@assets_app.callback(no_args_is_help=True)
def assets_callback() -> None:
    """
    Tool and demo asset tools.
    """
