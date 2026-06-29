from datetime import datetime

from pydantic import BaseModel


class Document(BaseModel):
    text: str
    created_date: datetime
    rubrics: list[str]


class DBDocument(BaseModel):
    id: int
    text: str
    created_date: datetime
    rubrics: list[str]


class TextMapping(BaseModel):
    id: int
    text: str
