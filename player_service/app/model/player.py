from pydantic import BaseModel
from typing import Optional
from uuid import UUID, uuid4


class Player(BaseModel):
    id: Optional[int] = int
    name: str
    age: int
    nickname: str
    discipline: str
    team: str
