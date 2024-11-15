import logging
from typing import Any

from .notion_page import NotionPage


class NotionParser:
    _logger = logging.getLogger(__name__)

    @classmethod
    def to_notion_page(cls, data: dict[str, Any]) -> NotionPage:
        try:
            identifier: str = data['id']
            title: str = data['properties']['title']['title'][0]['plain_text']

            return NotionPage(identifier=identifier, title=title)

        except Exception as ex:
            cls._logger.exception(str(ex), exc_info=True)
            raise
