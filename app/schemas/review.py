from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class ReviewedOption(BaseModel):
    id: int
    option_text: str
    is_correct: bool

    class Config:
        from_attributes = True

class ReviewedQuestion(BaseModel):
    id: int
    content: str
    question_type: str
    explanation: str

    user_selected_option_id: Optional[int] = None
    options: List[ReviewedOption] = []

    user_answer: Optional[str] = None
    expected_answer: Optional[str] = None
    is_correct: Optional[bool] = None

    class Config:
        from_attributes = True


class QuizReview(BaseModel):
    quiz_id: int
    quiz_title: str
    taken_at: datetime
    score: float
    correct_count: int
    total_questions: int
    questions: List[ReviewedQuestion]

    class Config:
        from_attributes = True
