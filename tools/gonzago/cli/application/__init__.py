import typer

from .publish import publish

application_app = typer.Typer()

application_app.command("publish")(publish)


@application_app.callback(no_args_is_help=True)
def application_callback() -> None:
    """
    Application asset tools.
    """
