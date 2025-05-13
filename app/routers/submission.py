from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.auth.auth import get_current_user
from app.crud.quiz import get_quiz_with_questions
from app.crud.submission import evaluate_answers, save_user_quiz_result
from app.crud.progress import update_user_skill_score
from app.schemas.submission import SubmitQuizRequest
from app.models.user import User

router = APIRouter(tags=["📤 Quiz Gönderimi"])

@router.post("/submit-quiz")
def submit_quiz(
    payload: SubmitQuizRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Quiz cevaplarını alır, değerlendirir, sonucu ve cevapları kaydeder.
    Ardından kullanıcının beceri skorunu günceller.
    """
    quiz = get_quiz_with_questions(db, payload.quiz_id)
    if not quiz:
        return {"Error":"Quiz not found"}

    evaluated_answers, correct_count = evaluate_answers(quiz.questions, payload.answers)

    result, score = save_user_quiz_result(
        db=db,
        user_id=current_user.id,
        quiz=quiz,
        evaluated_answers=evaluated_answers,
        correct_count=correct_count
    )

    update_user_skill_score(
        db=db,
        user_id=current_user.id,
        skill_id=quiz.skill_id,
        score=score
    )

    return {
        "detail": "Quiz submitted successfully",
        "score": score,
        "result_id": result.id
    }