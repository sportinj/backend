from datetime import datetime

from pydantic import BaseModel


class Injury(BaseModel):
    uid: int
    name: str
    description: str | None
    start_date: datetime
    end_date: datetime | None

    class Config:
        orm_mode = True
