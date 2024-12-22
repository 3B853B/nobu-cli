import json
import logging
from pathlib import Path
from typing import Any

from nobu.clients.notion import NotionClient
from nobu.clients.notion.filters import (
    FilterProperty,
    FilterValue,
    QueryFilter,
)
from nobu.core.htb.entities import HtbMachine
from nobu.core.notion import NotionDatabase, NotionPage
from nobu.settings import Settings

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

    def add_htb_machine(self, machine: HtbMachine, db_id: str) -> None:
        try:
            template: Path = Path('notion-templates/pages/htb_machine.json')

            if not template.exists():
                raise ValueError('htb_machine.json template not found')

            with open(template, 'r', encoding='utf-8') as file:
                dict_template: dict[str, Any] = json.load(file)

            parent: dict[str, Any] = dict_template['parent']
            parent['database_id']: str = db_id

            properties: dict[str, Any] = dict_template['properties']
            properties['Name']['title'][0]['text'][
                'content'
            ]: str = machine.name
            properties['Difficulty']['select'][
                'name'
            ]: str = machine.difficulty_text
            properties['OS']['select']['name']: str = machine.os
            machine_url: str = (
                f'https://app.hackthebox.com/machines/{machine.name}'
            )
            properties['URL']['url']: str = machine_url
            release_date: str = machine.release.strftime('%Y-%m-%d')
            properties['Release Date']['date']['start']: str = release_date

            icon: dict[str, Any] = dict_template['icon']
            avatar_url: str = f'https://labs.hackthebox.com{machine.avatar}'
            icon['external']['url']: str = avatar_url

            self.client.create_page(
                parent=parent, properties=properties, icon=icon
            )

        except Exception as ex:
            self.logger.exception(str(ex), exc_info=True)
            raise

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
