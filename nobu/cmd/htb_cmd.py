from rich.table import Table

from nobu.commons import Printer
from nobu.core.htb import HtbService
from nobu.core.htb.entities import HtbMachine
from nobu.core.notion import NotionDatabase, NotionPage

from . import NobuCmd


class HtbCmd(NobuCmd):
    """
    Handle all HTB commands.
    """

    def __init__(self) -> None:
        """
        Initializes HtbCmd object.
        """
        super().__init__('htb')
        self.machines: list[HtbMachine] | None = None

    def do_add(self, line: str | None = None) -> bool:
        try:
            args: list[str] = line.split(' ')

            context: NotionDatabase | NotionPage | None = (
                NobuCmd.notion_context
            )
            if not context or not isinstance(context, NotionDatabase):
                Printer.err('no Notion database in use, please select one:')
                super().do_dbs()
                return False

            identifier: str = args[-1]
            if identifier.isdigit():
                identifier: int = int(identifier)
            else:
                Printer.err('invalid machine identifier')
                return False

            if not self.machines:
                service: HtbService = HtbService()
                self.machines = service.list_machines(
                    size=50, update=True, retired=False
                )

            machine: HtbMachine | None = None
            for item in self.machines:
                if identifier == item.id:
                    machine = item
                    break

            if not machine:
                Printer.err('machine not found')
                return False

            NobuCmd.notion.add_htb_machine(machine, context.identifier)
            Printer.suc(
                f'machine {machine.name} added to {context.title} database'
            )

        except Exception as ex:
            Printer.err(str(ex))

    def do_machines(self, line: str | None = None) -> None:
        try:
            args: list[str] = line.split(' ')
            update: bool = '-u' in args
            retired: bool = '-r' in args
            size: int = int(args[args.index('-s') + 1]) if '-s' in args else 5

            service: HtbService = HtbService()
            self.machines: list[HtbMachine] = service.list_machines(
                size=size, update=update, retired=retired
            )

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
                    table.add_column(
                        column, header_style='b', justify='center'
                    )

            for machine in self.machines:
                table.add_row(
                    str(machine.id),
                    machine.name,
                    machine.difficulty_text,
                    machine.os,
                    str(machine.stars),
                    str(machine.user_owns_count),
                    str(machine.root_owns_count),
                )

            Printer.table(table)

        except Exception as ex:
            Printer.err(str(ex))

    def help_add(self) -> None:
        """
        Prints help menu for the add command.
        """
        help_text: str = """
        [bold cyan]Usage:[/bold cyan] add [OPTIONS] [ID]

        Add machine to Notion database.

        [bold cyan]Options:[/bold cyan]
            -a          Add all active machines.
        """
        Printer.help(help_text)

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
        Printer.help(help_text)
