from pydantic import BaseModel


class EmailContent(BaseModel):
    title: str
    text: str
