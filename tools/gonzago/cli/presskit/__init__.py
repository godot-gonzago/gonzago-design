import typer

from .publish import publish

presskit_app = typer.Typer()

presskit_app.command("publish")(publish)


@presskit_app.callback(no_args_is_help=True)
def presskit_callback() -> None:
    """
    Presskit tools.
    """
