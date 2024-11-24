import textwrap

from rich.console import Console
from rich.table import Table

from parabellum.commons import Printer
from parabellum.core.htb import HtbMachine, HtbService

from .base_cmd import BaseCmd
from .notion_cmd import NotionCmd


class ParabellumCmd(BaseCmd):
    """
    Handle all Parabellum commands.
    """

    def __init__(self) -> None:
        """
        Initializes ParabellumCmd object.
        """
        self.console: Console = Console()
        self.prompt: str = 'parabellum > '
        self.notion_cmd: NotionCmd = NotionCmd(self.prompt)
        super().__init__()

    def _print_machines(self, machines: list[HtbMachine]) -> None:
        table: Table = Table()
        columns: list[str] = [
            'ID',
            'Machine',
            'Difficulty',
            'OS',
            'Rating',
            'User Owns',
            'System Owns',
        ]

        for index, column in enumerate(columns):
            if index == 1:
                table.add_column(column, header_style='b', justify='left')
            elif index == len(columns):
                table.add_column(column, header_style='b', justify='right')
            else:
                table.add_column(column, header_style='b', justify='center')

        for machine in machines:
            table.add_row(
                str(machine.id),
                machine.name,
                machine.difficulty_text,
                machine.os,
                str(machine.stars),
                str(machine.user_owns_count),
                str(machine.root_owns_count),
            )

        self.console.print(table)

    def do_machines(self, line: str | None = None) -> None:
        try:
            args: list[str] = line.split(' ')
            update: bool = '-u' in args
            retired: bool = '-r' in args
            size: int = int(args[args.index('-s') + 1]) if '-s' in args else 5

            service: HtbService = HtbService()
            machines: list[HtbMachine] = service.list_machines(
                size=size, update=update, retired=retired
            )
            self._print_machines(machines)

        except Exception as ex:
            Printer.err(str(ex))

    def do_notion(self, line: str | None = None) -> None:
        try:
            self.notion_cmd.cmdloop()
        except Exception as ex:
            Printer.err(str(ex))

    def help_machines(self) -> None:
        """
        Prints help menu for the machines command.
        """
        help_text: str = """
        [bold cyan]Usage:[/bold cyan] machines [OPTIONS]

        List active and retired machines. By default it lists
        only active machines.

        [bold cyan]Options:[/bold cyan]
            -r          List only retired machines.
            -s  int     Max size of machines to be printed. Default is 5.
            -u          Force update results rather than getting from cache.
        """
        self.console.print(textwrap.dedent(help_text), highlight=False)

    def help_notion(self) -> None:
        """
        Prints help menu for the notion command.
        """
        help_text = """
        [bold cyan]Usage:[/bold cyan] notion

        Starts the Notion module and its commands.
        """
        self.console.print(textwrap.dedent(help_text), highlight=False)
