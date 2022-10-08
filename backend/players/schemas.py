from pydantic import BaseModel

class Player(BaseModel):
    uid: int
    name: str
    description: str