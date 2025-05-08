from pydantic import BaseModel
from typing import List
from datetime import datetime
from typing import Optional

  
class UserAnswerIn(BaseModel):
    question_id: int
    selected_option_id: Optional[int] = None  # Çoktan seçmeli için
    written_answer: Optional[str] = None      # Açık uçlu için

class SubmitQuizRequest(BaseModel):
    quiz_id: int
    answers: List[UserAnswerIn]
    

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
    user_selected_option_id: Optional[int]  # 👈 bu satır!
    options: List[ReviewedOption]

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
