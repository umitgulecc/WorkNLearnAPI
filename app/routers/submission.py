from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.crud.user import update_user_level
from app.database import get_db
from app.auth.auth import get_current_user
from app.crud.quiz import get_quiz_with_questions
from app.crud.submission import evaluate_answers, save_user_quiz_result
from app.crud.progress import update_user_skill_score
from app.models.question import Question
from app.models.quiz import Quiz
from app.models.user_answer import UserAnswer
from app.models.user_quiz_result import UserQuizResult
from app.schemas.submission import SubmitQuizRequest
from app.models.user import User
from app.crud.personalized_quiz import create_personalized_placement_quiz


router = APIRouter(tags=["📤 Quiz Gönderimi"])
LEVEL_UP_SCORE_THRESHOLD = 20 

@router.post("/submit-quiz")
def submit_quiz(
    payload: SubmitQuizRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    quiz = get_quiz_with_questions(db, payload.quiz_id)
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")

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
    from app.crud.user import get_user_total_score

    total_score = get_user_total_score(db, current_user.id)

    if total_score >= LEVEL_UP_SCORE_THRESHOLD:
        print("✅ Level-up placement test için hazır!")
        
    
    LEVEL_PASS_SCORE = 0.7
    NEXT_LEVEL_ID = current_user.level_id + 1

    if quiz.quiz_type_id == 1: # Yerleştirme sınavı
        if score >= LEVEL_PASS_SCORE:
            update_user_level(db, current_user.id, NEXT_LEVEL_ID)
            print("✅ Seviye atladı!")
        else:
            print("❌ Seviye atlama sınavından kaldı, GPT'den özel sınav hazırlanacak.")
            try:
                new_quiz = create_personalized_placement_quiz(db, current_user)
                return {
                    "detail": "Placement sınavı başarısız. GPT destekli kişisel sınav oluşturuldu.",
                    "score": score,
                    "new_quiz_id": new_quiz.id
                }
            except ValueError:
                return {
                    "detail": "Zayıf konu bulunamadı, GPT sınavı oluşturulamadı.",
                    "score": score
                }
            

    
    return {
        "detail": "Quiz submitted successfully",
        "score": score,
        "result_id": result.id
    }
