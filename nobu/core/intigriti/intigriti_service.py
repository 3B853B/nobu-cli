import logging
from typing import Any

from nobu.clients.intigriti import IntigritiClient
from nobu.settings import Settings

from .entities import IntigritiProgram, IntigritiProgramSlim
from .intigriti_parser import IntigritiParser


class IntigritiService:
    def __init__(self) -> None:
        """
        Initializes all IntigritiService object attributes.

        :raise ValueError: When Intigriti token is not found.
        """
        self.logger: logging.Logger = logging.getLogger(
            self.__class__.__name__
        )
        self.settings: Settings = Settings()
        self.token: str = (
            None
            if not self.settings.intigriti_token
            else self.settings.intigriti_token
        )

        if not self.token:
            raise ValueError('could not find Intigriti token')

        self.client = IntigritiClient(token=self.token)

    def list_programs(self) -> list[IntigritiProgramSlim]:
        """
        Lists all Intigriti programs for your user.

        :return: A list of programs.

        :raise Exception: When an unexpected error occurs.
        """
        limit: int = 50
        offset: int = 0
        records: list[dict[str, Any]] = []

        while True:
            response: dict[str, Any] = self.client.get_all_programs(
                limit=limit, offset=offset
            )
            offset += limit
            records.extend(response['records'])

            if offset >= response['maxCount']:
                break

        programs: list[IntigritiProgramSlim] = [
            IntigritiParser.to_program_slim(record) for record in records
        ]

        return programs

    def get_program(self, program_id: str) -> IntigritiProgram:
        """
        Gets program information.

        :return: A program with its information.

        :raise Exception: When an unexpected error occurs.
        """
        try:
            response: dict[str, Any] = self.client.get_program_details(
                program_id=program_id
            )

            return IntigritiParser.to_program(response)

        except Exception as ex:
            self.logger.exception(str(ex), exc_info=True)
            raise
