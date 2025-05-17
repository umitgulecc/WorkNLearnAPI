from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.auth.auth import get_current_user
from app.models.user import User
from app.crud.personalized_quiz import create_personalized_quiz

router = APIRouter(prefix="/personalized-quiz", tags=["🎯 Kişiye Özel Quiz"])

@router.post("/generate")
def generate_quiz_for_user(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    quiz = create_personalized_quiz(db, user_id=current_user.id)
    if not quiz:
        raise HTTPException(status_code=404, detail="Yeterli veri yok veya zayıf konu bulunamadı.")
    

    return {
        "message": "📌 Kişisel quiz başarıyla oluşturuldu.",
        "quiz_id": quiz.id,
        "title": quiz.title
    }
