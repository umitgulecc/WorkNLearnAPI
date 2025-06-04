from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.auth.auth import get_current_user
from app.crud.review import get_quiz_review
from app.models.user import User
from app.models.user_quiz_result import UserQuizResult
from app.schemas.review import QuizReview
from app.utils.permissions import has_access_to_user

router = APIRouter(tags=["🔍 Quiz İncelemesi"])



@router.get("/review-quiz/{result_id}", response_model=QuizReview)
def review_quiz(
    result_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = db.query(UserQuizResult).filter_by(id=result_id).first()
    if not result:
        raise HTTPException(status_code=404, detail="Sonuç bulunamadı.")

    target_user = db.query(User).filter_by(id=result.user_id).first()
    if not has_access_to_user(current_user, target_user):
        raise HTTPException(status_code=403, detail="Bu sonucu görme yetkiniz yok.")

    return get_quiz_review(db, user_id=result.user_id, result_id=result_id)
