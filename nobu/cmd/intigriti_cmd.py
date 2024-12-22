from rich.table import Table

from nobu.commons import Printer
from nobu.core.intigriti import IntigritiService
from nobu.core.intigriti.entities import IntigritiProgram, IntigritiProgramSlim

from .nobu_cmd import NobuCmd


class IntigritiCmd(NobuCmd):
    """
    Handle the Intigriti module commands.
    """

    def __init__(self) -> None:
        """
        Initializes IntigritiCmd object.
        """
        super().__init__('intigriti')
        self.programs: list[IntigritiProgramSlim | None] = None

    def do_info(self, line: str | None = None) -> bool:
        try:
            args: list[str] = line.split(' ')

            identifier: str = args[-1]
            if not identifier:
                Printer.err('invalid program identifier')
                return False

            if not self.programs:
                service: IntigritiService = IntigritiService()
                self.programs = service.list_programs()

            program: IntigritiProgram | None = None
            for item in self.programs:
                if identifier == item.id:
                    service: IntigritiService = IntigritiService()
                    program = service.get_program(item.id)
                    break

            if not program:
                Printer.err('program not found')
                return False

            table = Table()

            columns: list[str] = [
                'Domain',
                'Tier',
                'Type',
                'Description',
            ]

            for index, column in enumerate(columns):
                if index == 1:
                    table.add_column(column, header_style='b', justify='left')
                elif index == len(columns):
                    table.add_column(column, header_style='b', justify='right')
                else:
                    table.add_column(column, header_style='b', justify='full')

            for domain in program.domains:
                table.add_row(
                    domain.endpoint,
                    domain.tier,
                    domain.type,
                    domain.description,
                )

            Printer.table(table)

        except Exception as ex:
            Printer.err(str(ex))

    def do_programs(self, line: str | None = None) -> None:
        try:
            service: IntigritiService = IntigritiService()
            self.programs = service.list_programs()

            table: Table = Table()
            columns: list[str] = [
                'ID',
                'Name',
                'Status',
                'Confidentiality',
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

            for program in self.programs:
                table.add_row(
                    program.id,
                    program.name,
                    program.status,
                    program.confidentiality_level,
                )

            Printer.table(table)
        except Exception as ex:
            Printer.err(str(ex))

    def help_info(self) -> None:
        """
        Prints help menu for the info command.
        """
        help_text = """
        [bold cyan]Usage:[/bold cyan] info <PROGRAM-ID>

        Get program information.
        """
        Printer.help(help_text)

    def help_programs(self) -> None:
        """
        Prints help menu for the programs command.
        """
        help_text = """
        [bold cyan]Usage:[/bold cyan] programs

        List all Intigriti available programs for your user.
        """
        Printer.help(help_text)
