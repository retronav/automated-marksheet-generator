import traceback
from util.log import error
from commands.email import email
from commands.generate import generate
import click
from colorama import Fore

print = click.echo


@click.group(invoke_without_command=True)
@click.option(
    "--verbose",
    "-v",
    default=False,
    is_flag=True,
    help="Enable verbose/debug level logging.",
)
@click.pass_context
def cli(ctx: click.Context, verbose):
    if ctx.invoked_subcommand is None:
        print(
            Fore.MAGENTA
            + "This is rep, a simple, fast, yet customizable CLI to generate report cards of students and send them to their email addresses. "
            + Fore.RESET
        )
        print(ctx.get_help())
    if verbose:
        print("Verbose logging is enabled")


cli.add_command(generate)
cli.add_command(email)


if __name__ == "__main__":
    try:
        cli()
    except Exception as e:
        traceback.print_exc()
        error("Some fatal error happened in the CLI. Terminating...", 1)
