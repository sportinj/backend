from pydantic import BaseModel

class Team(BaseModel):
    uid: int
    name: str
