from pydantic import BaseModel


class RequestCreate(BaseModel):
    title: str
    service: str
    comment: str
    date: str = None
    is_archived: bool = False


class RequestUpdate(BaseModel):
    title: str
    service: str
    comment: str
    date: str = None
    is_archived: bool = False
