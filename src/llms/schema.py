from pydantic import BaseModel


class Links(BaseModel):
    url: str
    title: str