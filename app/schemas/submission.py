from pydantic import BaseModel
from typing import Optional
from typing import List

class UserAnswerIn(BaseModel):
    question_id: int
    selected_option_id: Optional[int] = None 
    written_answer: Optional[str] = None  
    

class SubmitQuizRequest(BaseModel):
    quiz_id: int
    answers: List[UserAnswerIn]
    