import logging
from typing import Any

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
    ) -> dict[str, Any]:
        try:
            resource_url: str = f'{self.base_url}/search'

            headers: dict[str, str] = self.base_headers
            headers['Content-Type']: str = 'application/json'

            body: dict[str, Any] = {
                'query': query,
                'sort': query_sort.model_dump() if query_sort else None,
                'filter': query_filter.model_dump() if query_filter else None,
                'start_cursor': start_cursor,
                'page_size': page_size,
            }

            body: dict[str, Any] = {
                key: value for key, value in body.items() if value is not None
            }

            results: list[dict[str, Any]] = []
            while True:
                response: requests.Response = requests.post(
                    url=resource_url,
                    headers=headers,
                    json=body,
                    timeout=self.timeout,
                )

                response.raise_for_status()

                dict_response: dict[str, Any] = response.json()
                results.extend(dict_response['results'])

                has_more: bool = dict_response['has_more']
                if has_more:
                    body['start_cursor']: str = dict_response['next_cursor']
                else:
                    dict_response['results']: list[dict[str, Any]] = results
                    return dict_response

        except Exception as ex:
            self.logger.exception(str(ex), exc_info=True)
            raise
