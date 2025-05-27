from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.auth.auth import get_current_user
from app.models.user_quiz_result import UserQuizResult
from app.models.user import User

router = APIRouter(tags=["📊 İstatistik"])

@router.get("/me/summary-stats")
def get_user_summary_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    results = db.query(UserQuizResult).filter_by(user_id=current_user.id).all()

    total_correct = sum(r.correct_count for r in results)
    total_questions = sum(r.total_questions for r in results)
    total_wrong = total_questions - total_correct

    return {
        "user_id": current_user.id,
        "total_quizzes": len(results),
        "total_correct": total_correct,
        "total_wrong": total_wrong,
        "total_questions": total_questions
    }
