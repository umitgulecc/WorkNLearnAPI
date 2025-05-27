from pydantic import BaseModel
from typing import Optional, List

class QuizOverview(BaseModel):
    id: int
    title: str
    description: Optional[str] = ""  
    skill_id: int
    level_id: int
    is_placement_test: bool

    class Config:
        from_attributes = True


class QuestionOptionOut(BaseModel):
    id: int
    option_text: str

    class Config:
        from_attributes = True


class QuizQuestionOut(BaseModel):
    id: int
    content: str
    explanation: Optional[str]
    question_type: str
    options: List[QuestionOptionOut]
    reading_passage_title: Optional[str] = None
    reading_passage_content: Optional[str] = None
    class Config:
        from_attributes = True


class QuizDetailOut(BaseModel):
    id: int
    title: str
    description: Optional[str]
    questions: List[QuizQuestionOut]

    class Config:
        from_attributes = True




class QuizOverviewWithResultId(BaseModel):
    quiz_id: int
    title: str
    level_id: int
    result_id: int

    class Config:
        from_attributes = True

