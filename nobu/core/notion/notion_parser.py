import logging
from typing import Any

from nobu.commons import DictUtils

from .notion_database import NotionDatabase
from .notion_page import NotionPage


class NotionParser:
    _logger: logging.Logger = logging.getLogger(__name__)

    @classmethod
    def to_notion_database(cls, data: dict[str, Any]) -> NotionDatabase:
        try:
            identifier: str = data['id']
            title: str = data['title'][0]['plain_text']

            return NotionDatabase(identifier=identifier, title=title)

        except Exception as ex:
            cls._logger.exception(str(ex), exc_info=True)
            raise

    @classmethod
    def to_notion_page(cls, data: dict[str, Any]) -> NotionPage:
        try:
            identifier: str = data['id']
            titles: list[dict[str, Any]] | dict[str, Any] = DictUtils.get_key(
                data, 'title'
            )

            if isinstance(titles, list):
                title: str = titles[0]['plain_text']
            else:
                title: str = titles['title'][0]['plain_text']

            return NotionPage(identifier=identifier, title=title)

        except Exception as ex:
            cls._logger.exception(str(ex), exc_info=True)
            raise
