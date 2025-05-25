from pydantic import BaseModel
from datetime import datetime

class TeamResult(BaseModel):
    user_id: int
    full_name: str
    quiz_title: str
    score: int
    taken_at: datetime

    class Config:
        from_attributes = True


class TeamMemberSummary(BaseModel):
    user_id: int
    full_name: str
    level: str
    total_quizzes: int
    average_score: float
    total_score: float
    class Config:
        from_attributes = True