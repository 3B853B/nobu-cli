import logging
from typing import Any

from parabellum.clients.notion import NotionClient
from parabellum.clients.notion.filters import (
    FilterProperty,
    FilterValue,
    QueryFilter,
)
from parabellum.core import NotionDatabase, NotionPage
from parabellum.settings import Settings

from .notion_parser import NotionParser


class NotionService:
    def __init__(self) -> None:
        self.logger: logging.Logger = logging.getLogger(
            self.__class__.__name__
        )
        self.settings: Settings = Settings()
        self.token: str = self.settings.notion_token

        if not self.token:
            raise ValueError('could not find Notion token')

        self.client: NotionClient = NotionClient(token=self.token)

    def list_dbs(self) -> list[NotionDatabase]:
        try:
            response: dict[str, Any] = self.client.search_by_title(
                query='',
                query_filter=QueryFilter(
                    value=FilterValue.DATABASE, property=FilterProperty.OBJECT
                ),
            )

            dbs: list[NotionDatabase] = []
            for result in response['results']:
                dbs.append(NotionParser.to_notion_database(result))

            return dbs

        except Exception as ex:
            self.logger.exception(str(ex), exc_info=True)
            raise

    def list_pages(self) -> list[NotionPage]:
        try:
            response: dict[str, Any] = self.client.search_by_title(
                query='',
                query_filter=QueryFilter(
                    value=FilterValue.PAGE, property=FilterProperty.OBJECT
                ),
            )

            pages: list[NotionPage] = []
            for result in response['results']:
                pages.append(NotionParser.to_notion_page(result))

            return pages

        except Exception as ex:
            self.logger.exception(str(ex), exc_info=True)
            raise
