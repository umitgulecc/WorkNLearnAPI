import datetime
from sqlalchemy.orm import Session
from app.database import get_db
from app.auth.auth import get_current_user
from fastapi import APIRouter, Depends
from app.schemas.user_result import SubmitQuizRequest
from app.crud.user_result import evaluate_and_save_quiz
from app.crud.user_result import get_quiz_review
from app.schemas.user_result import QuizReview
from app.models.user_skill_score import UserSkillScore
from app.models.quiz import Quiz


router = APIRouter()
@router.post("/submit-quiz")
def submit_quiz(
    payload: SubmitQuizRequest,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # 1. Quiz değerlendirme ve kayıt
    result = evaluate_and_save_quiz(
        db=db,
        user_id=current_user.id,
        quiz_id=payload.quiz_id,
        answers=payload.answers
    )

    # 2. Quiz'in skill_id'sini al
    quiz = db.query(Quiz).filter_by(id=payload.quiz_id).first()

    # 3. Kullanıcının beceri skorunu güncelle
    update_user_skill_score(
        db=db,
        user_id=current_user.id,
        skill_id=quiz.skill_id,
        score=result["score"]
    )

    return result
    
@router.get("/review-quiz/{result_id}", response_model=QuizReview)
def review_quiz(
    result_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return get_quiz_review(db, current_user.id, result_id)



def update_user_skill_score(db: Session, user_id: int, skill_id: int, score: float):
    existing = db.query(UserSkillScore).filter_by(user_id=user_id, skill_id=skill_id).first()
    if existing:
        existing.total_score += score
        existing.updated_at = datetime.datetime.utcnow()
    else:
        new_score = UserSkillScore(
            user_id=user_id,
            skill_id=skill_id,
            total_score=score
        )
        db.add(new_score)
    db.commit()
