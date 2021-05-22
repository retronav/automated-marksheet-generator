from colorama import Fore
from colorama import Fore
from click import echo as print


def log(thing):
    """
    Prints a log message in the terminal.
    """
    print(Fore.CYAN + f"LOG: {thing}" + Fore.RESET)


def error(thing, exitCode):
    """
    Prints a error message in the terminal.
    """
    print(Fore.RED + f"ERROR: {thing}" + Fore.RESET)
    if exitCode:
        exit(exitCode)
