from sqlalchemy.orm import Session
from app.database import get_db
from app.auth.auth import get_current_user
from app.models.question_type import QuestionType
from app.schemas.quiz import QuestionOptionOut, QuizDetailOut, QuizOverview, QuizQuestionOut
from app.crud.quiz import get_quizzes_by_filters
from fastapi import APIRouter, Depends, HTTPException
from app.crud.quiz import get_quiz_with_questions

router = APIRouter(prefix="/quiz", tags=["🧪 Quiz İşlemleri"])

@router.get("/quizzes", response_model=list[QuizOverview])
def list_quizzes(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
    quiz_type_id: int | None = None,
    skill_id: int | None = None,
    level_id: int | None = None
):
    quizzes = get_quizzes_by_filters(
        db=db,
        user_level_id=current_user.level_id,
        quiz_type_id=quiz_type_id,
        skill_id=skill_id,
        level_id=level_id
    )
    return quizzes

@router.get("/quiz/{quiz_id}", response_model=QuizDetailOut)
def get_quiz_detail(quiz_id: int, db: Session = Depends(get_db)):
    quiz = get_quiz_with_questions(db, quiz_id)
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")

    return QuizDetailOut(
        id=quiz.id,
        title=quiz.title,
        description=quiz.description,
        questions=[
            QuizQuestionOut(
                id=q.id,
                content=q.content,
                explanation=q.explanation,
                question_type=q.question_type.type_name,
                options=[
                    QuestionOptionOut(id=o.id, option_text=o.option_text)
                    for o in q.options
                ]
            ) for q in quiz.questions
        ]
    )
