import logging
from datetime import timedelta
from typing import Any

from requests_cache import CachedResponse, CachedSession, OriginalResponse

from nobu.commons import BearerAuth


class HtbClient:
    def __init__(self, token: str, timeout: int = 30) -> None:
        """
        Initializes all HtbClient object attributes.

        :param token: User bearer token.
        :param timeout: Timeout for HTTP requests. Default is 30
         seconds.
        """
        self.logger: logging.Logger = logging.getLogger(
            self.__class__.__name__
        )
        self.token: str = token
        self.base_url: str = 'https://labs.hackthebox.com/api/v4'
        self.base_headers: dict[str, str] = {
            'User-Agent': 'Nobu',
            'Accept': 'application/json',
        }
        self.session: CachedSession = CachedSession(
            cache_name='.cache',
            backend='filesystem',
            expire_after=timedelta(minutes=5),
        )
        self.timeout: int = timeout

    def list_machines(
        self, size: int = 100, retired: bool = False, update: bool = False
    ) -> dict[str, Any]:
        """
        Lists machines.

        :param size: Quantity of machines to be returned.
        :param retired: List only retired machines.
        :param update: Force update the result rather than getting
         from cache.

        :return: A dictionary containing a list of machines.

        :raise ValueError: When size value is lesser than 0.
        """
        if size < 0:
            raise ValueError('size value cannot be lesser than 0.')

        try:
            resource_url: str = (
                'machine/paginated'
                if not retired
                else 'machine/list/retired/paginated'
            )
            url: str = f'{self.base_url}/{resource_url}'

            if update:
                [
                    self.session.cache.delete(urls=[item])
                    for item in self.session.cache.urls()
                    if url in item
                ]

            results: dict[str, Any] = {}
            machines: list[dict[str, Any]] = []
            min_size: int = 5
            max_size: int = 100
            per_page: int = max_size if size < min_size else max_size
            while len(machines) < size:
                params: dict[str, int] = {'per_page': per_page}

                response: OriginalResponse | CachedResponse = self.session.get(
                    url=url,
                    headers=self.base_headers,
                    params=params,
                    timeout=self.timeout,
                    auth=BearerAuth(self.token),
                )

                response.raise_for_status()

                results: dict[str, Any] = response.json()
                machines.extend(results['data'])

                links: dict[str, str] = results['links']
                if not links['next']:
                    break

                url: str = links['next']

            results['data']: list[str, Any] = machines[:size]
            return results

        except Exception as ex:
            self.logger.exception(str(ex), exc_info=True)
            raise
