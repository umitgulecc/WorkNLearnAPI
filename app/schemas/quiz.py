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

class Option(BaseModel):
    id: int
    option_text: str

    class Config:
        from_attributes = True  # Pydantic V2 uyumlu

class QuestionDetail(BaseModel):
    id: int
    content: str
    question_type: str
    options: List[Option]

    class Config:
        from_attributes = True
