from pydantic import BaseModel


class Player(BaseModel):
    uid: int
    name: str
    description: str
    team_id: int

    class Config:
        orm_mode = True
