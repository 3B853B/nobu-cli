import json
import logging
from pathlib import Path
from typing import Any

from parabellum.clients.notion import NotionClient
from parabellum.clients.notion.filters import (
    FilterProperty,
    FilterValue,
    QueryFilter,
)
from parabellum.core.notion import NotionDatabase, NotionPage
from parabellum.settings import Settings

from .notion_parser import NotionParser


class NotionService:
    def __init__(self) -> None:
        self.logger: logging.Logger = logging.getLogger(
            self.__class__.__name__
        )
        self.settings: Settings = Settings()
        self.token: str = self.settings.notion_token
        self.root_page_id: str | None = self.settings.notion_root_page_id

        if not self.token:
            raise ValueError('could not find Notion token')

        self.client: NotionClient = NotionClient(token=self.token)

    def create_db(self, template: Path, parent_id: str | None = None) -> None:
        try:
            if not self.root_page_id and not parent_id:
                raise ValueError('could not find any parent ID')

            if not template.exists():
                raise ValueError('file not found')

            with open(template, 'r', encoding='utf-8') as file:
                dict_template: dict[str, Any] = json.load(file)

            parent = dict_template['parent']
            parent['page_id'] = (
                self.root_page_id if not parent_id else parent_id
            )

            self.client.create_database(
                parent=parent,
                properties=dict_template['properties'],
                icon=dict_template.get('icon'),
                cover=dict_template.get('cover'),
                title=dict_template.get('title'),
            )

        except ValueError:
            self.logger.exception('invalid template format')
            raise

        except Exception as ex:
            self.logger.exception(str(ex), exc_info=True)
            raise

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
