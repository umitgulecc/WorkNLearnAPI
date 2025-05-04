from sqlalchemy.orm import Session
from app.database import get_db
from app.auth.auth import get_current_user
from app.schemas.quiz import QuizOverview
from app.crud.quiz import get_quizzes_by_user_level
from fastapi import APIRouter, Depends, HTTPException
from app.crud.quiz import get_quiz_with_questions
from app.schemas.user_result import QuizDetail

router = APIRouter()

@router.get("/quizzes", response_model=list[QuizOverview])
def list_quizzes(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return get_quizzes_by_user_level(db, current_user.level_id)

@router.get("/quiz/{quiz_id}", response_model=QuizDetail)
def get_quiz_detail(quiz_id: int, db: Session = Depends(get_db)):
    quiz = get_quiz_with_questions(db, quiz_id)
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    return quiz
