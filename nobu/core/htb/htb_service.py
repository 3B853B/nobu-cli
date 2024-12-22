import logging
from typing import Any

from nobu.clients.htb import HtbClient
from nobu.settings import Settings

from .entities import HtbMachine
from .htb_parser import HtbParser


class HtbService:
    def __init__(self) -> None:
        """
        Initializes all HtbService object attributes.

        :raise ValueError: When HTB token is not found.
        """
        self.logger: logging.Logger = logging.getLogger(
            self.__class__.__name__
        )
        self.settings: Settings = Settings()
        self.token: str = self.settings.htb_token

        if not self.token:
            raise ValueError('could not find HTB token')

        self.client: HtbClient = HtbClient(token=self.token)

    def list_machines(
        self, size: int, update: bool, retired: bool
    ) -> list[HtbMachine]:
        """
        Lists HTB machines.

        :param size: Quantity of machines to be returned.
        :param retired: List only retired machines.
        :param update: Force update the result rather than getting
         from cache.

        :return: List of machine objects.

        :raise Exception: When an unexpected error occurs.
        """
        try:
            response: dict[str, Any] = self.client.list_machines(
                size=size, update=update, retired=retired
            )

            machines = HtbParser.to_machine_list(response)
            machines.sort(reverse=True)

            return machines

        except Exception as ex:
            self.logger.exception(str(ex), exc_info=True)
            raise
