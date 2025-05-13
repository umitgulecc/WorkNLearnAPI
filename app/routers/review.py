from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.auth.auth import get_current_user
from app.crud.review import get_quiz_review
from app.models.user import User
from app.schemas.review import QuizReview

router = APIRouter(tags=["🔍 Quiz İncelemesi"])



@router.get("/review-quiz/{result_id}", response_model=QuizReview)
def review_quiz(
    result_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Kullanıcının çözmüş olduğu quiz'e ait cevapları, açıklamaları ve doğruluk durumunu döner.
    """
    return get_quiz_review(db, user_id=current_user.id, result_id=result_id)