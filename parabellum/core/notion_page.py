from pydantic import BaseModel


class NotionPage(BaseModel):
    identifier: str
    title: str
