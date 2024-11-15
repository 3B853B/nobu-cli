import logging
import typing

import requests

from .filters.query_filter import QueryFilter
from .sorts.query_sort import QuerySort


class NotionClient:
    def __init__(
        self, token: str, version: str = '2022-06-28', timeout: int = 30
    ) -> None:
        self.logger: logging.Logger = logging.getLogger(
            self.__class__.__name__
        )
        self.token: str = token
        self.base_url: str = 'https://api.notion.com/v1'
        self.base_headers: dict[str, str] = {
            'Notion-Version': version,
            'Authorization': f'Bearer {token}',
        }
        self.timeout: int = timeout

    def search_by_title(
        self,
        query: str,
        query_sort: QuerySort | None = None,
        query_filter: QueryFilter | None = None,
        start_cursor: str | None = None,
        page_size: int | None = None,
    ) -> dict[str, typing.Any]:
        try:
            resource_url: str = f'{self.base_url}/search'

            headers: dict[str, str] = self.base_headers
            headers['Content-Type']: str = 'application/json'

            body_params: dict[str, typing.Any] = {
                'query': query,
                'sort': query_sort.model_dump() if query_sort else None,
                'filter': query_filter.model_dump() if query_filter else None,
                'start_cursor': start_cursor,
                'page_size': page_size,
            }

            body_params: dict[str, typing.Any] = {
                key: value
                for key, value in body_params.items()
                if value is not None
            }

            results: list[dict[str, typing.Any]] = []
            while True:
                response: requests.Response = requests.post(
                    url=resource_url,
                    headers=headers,
                    json=body_params,
                    timeout=self.timeout,
                )

                response.raise_for_status()

                dict_response = response.json()
                results.extend(dict_response['results'])

                has_more = dict_response['has_more']
                if has_more:
                    body_params['start_cursor'] = dict_response['next_cursor']
                else:
                    dict_response['results'] = results
                    return dict_response

        except Exception as ex:
            self.logger.exception(str(ex), exc_info=True)
            raise
