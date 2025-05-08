from pydantic import BaseModel
from typing import List

class QuizOverview(BaseModel):
    id: int
    title: str
    description: str
    skill_id: int
    level_id: int
    is_placement_test: bool

    class Config:
        orm_mode = True

