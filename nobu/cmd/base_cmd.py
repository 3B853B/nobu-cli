import cmd
import os
import sys
from typing import Any, Callable

from nobu.commons import Printer


class BaseCmd(cmd.Cmd):
    """
    Defines a common way to handle the most used methods in Cmd class.
    """

    def __init__(self) -> None:
        """
        Initializes BaseCmd object.
        """
        super().__init__()

    def get_option_value(
        self, args: list[str], option: str, convert_to: Callable
    ) -> Any | None:
        """
        Gets the value from an option and converts it to the
        specified callable type.

        :param args: List of arguments.
        :param option: Option to be searched.
        :param convert_to: Callable to be used as a converter.
        """
        if option in args:
            start_index: int = args.index(option) + 1
            values: list[Any] = []
            for i in range(start_index, len(args)):
                if args[i].startswith('-'):
                    break
                values.append(args[i])
            return convert_to(' '.join(values))

        return None

    def default(self, line: str) -> None:
        """
        Handles any input that is not known by the application.

        :param line: User input, default method argument for Cmd class.
        """
        Printer.err(f'unknown command: {line}')

    def do_clear(self, line: str | None = None) -> None:
        os.system('cls') if os.name == 'nt' else os.system('clear')

    def do_exit(self, line: str | None = None) -> None:
        sys.exit(0)

    def do_quit(self, line: str | None = None) -> None:
        self.do_exit()

    def emptyline(self) -> None:
        """
        Handles when an empty line is inputted.
        """
        pass

    def help_clear(self) -> None:
        """
        Prints help menu for the clear command.
        """
        help_text: str = """
        [bold cyan]Usage:[/bold cyan] clear

        Clears the application console.
        """
        Printer.help(help_text)

    def help_exit(self) -> None:
        """
        Prints help menu for the exit command.
        """
        help_text: str = """
        [bold cyan]Usage:[/bold cyan] exit

        Exits the application.
        """
        Printer.help(help_text)

    def help_quit(self) -> None:
        """
        Prints help menu for the quit command.
        """
        help_text: str = """
        [bold cyan]Usage:[/bold cyan] quit

        Exits the application.
        """
        Printer.help(help_text)
