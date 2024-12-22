import logging
from typing import Any

import requests


class IntigritiClient:
    def __init__(self, token: str, timeout: int = 30) -> None:
        """
        Initializes all IntigritiClient object attributes.

        :param token: User personal access token.
        :param timeout: Timeout for HTTP requests. Default is 30
         seconds.
        """
        self.logger: logging.Logger = logging.getLogger(
            self.__class__.__name__
        )
        self.token: str = token
        self.base_url: str = 'https://api.intigriti.com/external/researcher/v1'
        self.headers: dict[str, str] = {
            'User-Agent': 'Nobu',
            'Accept': 'application/json',
            'Authorization': f'Bearer {token}',
        }
        self.timeout: int = timeout

    def get_all_programs(
        self,
        following: bool | None = None,
        limit: int = 50,
        status_id: int | None = None,
        offset: int | None = None,
        type_id: int | None = None,
    ) -> dict[str, Any]:
        """
        Lists all Intigriti programs for your user.

        :param following: Indicates whether you are following the
         program.
        :param limit: Limit of programs to be returned.
        :param offset: Get programs starting by the specified offset.
        :param status_id: Current status of the program.
        :param type_id: Type of program.

        :return: A list of programs.

        :raise Exception: When an unexpected error occurs.
        """
        try:
            resource_url: str = f'{self.base_url}/programs'
            params: dict[str, Any] = {
                'following': following,
                'limit': limit,
                'offset': offset,
                'statusId': status_id,
                'typeId': type_id,
            }

            params: dict[str, Any] = {
                key: value
                for key, value in params.items()
                if value is not None
            }

            response: requests.Response = requests.get(
                url=resource_url,
                headers=self.headers,
                params=params,
                timeout=self.timeout,
            )

            response.raise_for_status()

            return response.json()

        except Exception as ex:
            self.logger.exception(str(ex), exc_info=True)
            raise

    def get_program_details(self, program_id: str) -> dict[str, Any]:
        """
        Gets program information.

        :param program_id: Program identifier.

        :return: A program with its information.

        :raise Exception: When an unexpected error occurs.
        """
        try:
            resource_url: str = f'{self.base_url}/programs/{program_id}'

            response: requests.Response = requests.get(
                url=resource_url,
                headers=self.headers,
                timeout=self.timeout,
            )

            response.raise_for_status()

            return response.json()

        except Exception as ex:
            self.logger.exception(str(ex), exc_info=True)
            raise
