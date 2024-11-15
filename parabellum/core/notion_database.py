from pydantic import BaseModel


class NotionDatabase(BaseModel):
    identifier: str
    title: str
