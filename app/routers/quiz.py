from sqlalchemy.orm import Session
from app.database import get_db
from app.auth.auth import get_current_user
from app.models.question_type import QuestionType
from app.schemas.quiz import QuizOverview
from app.crud.quiz import get_quizzes_by_user_level
from fastapi import APIRouter, Depends, HTTPException
from app.crud.quiz import get_quiz_with_questions

router = APIRouter()

@router.get("/quizzes", response_model=list[QuizOverview])
def list_quizzes(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return get_quizzes_by_user_level(db, current_user.level_id)

@router.get("/quiz/{quiz_id}")
def get_quiz_detail(quiz_id: int, db: Session = Depends(get_db)):
    quiz = get_quiz_with_questions(db, quiz_id)
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")

    # type name'leri hazırlıyoruz
    all_types = db.query(QuestionType).all()
    type_dict = {t.id: t.type_name for t in all_types}

    # Quiz detayını manuel oluştur
    quiz_data = {
        "id": quiz.id,
        "title": quiz.title,
        "description": quiz.description,
        "questions": []
    }

    for question in quiz.questions:
        quiz_data["questions"].append({
            "id": question.id,
            "content": question.content,
            "question_type": type_dict.get(question.question_type_id),
            "options": [
                {
                    "id": opt.id,
                    "option_text": opt.option_text,
                } for opt in question.options
            ]
        })

    return quiz_data
