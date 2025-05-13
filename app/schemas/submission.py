from pydantic import BaseModel
from typing import Optional
from typing import List

class UserAnswerIn(BaseModel):
    question_id: int
    selected_option_id: Optional[int] = None  # Çoktan seçmeli için
    written_answer: Optional[str] = None      # Açık uçlu için
    

class SubmitQuizRequest(BaseModel):
    quiz_id: int
    answers: List[UserAnswerIn]
    