from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.auth.auth import get_current_user
from app.models.user import User
from app.crud.personalized_quiz import create_personalized_quiz
from app.crud.personalized_quiz import create_personalized_placement_quiz
from app.crud.quiz import get_quiz_with_questions
from app.schemas.quiz import QuizDetailOut, QuestionOptionOut, QuizQuestionOut

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


@router.post("/placement-test", response_model=QuizDetailOut)
def generate_personalized_placement_quiz(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # GPT destekli kişisel placement test oluştur
    quiz = create_personalized_placement_quiz(db, current_user)
    if not quiz:
        raise HTTPException(status_code=400, detail="Quiz oluşturulamadı.")

    # Quiz detaylarını joinedload ile birlikte çek
    detailed_quiz = get_quiz_with_questions(db, quiz.id)
    if not detailed_quiz:
        raise HTTPException(status_code=404, detail="Quiz verisi yüklenemedi.")

    return QuizDetailOut(
        id=detailed_quiz.id,
        title=detailed_quiz.title,
        description=detailed_quiz.description,
        questions=[
            QuizQuestionOut(
                id=q.id,
                content=q.content,
                explanation=q.explanation,
                question_type=q.question_type.type_name,
                options=[
                    QuestionOptionOut(
                        id=opt.id,
                        option_text=opt.option_text
                    ) for opt in q.options
                ]
            ) for q in detailed_quiz.questions
        ]
    )
