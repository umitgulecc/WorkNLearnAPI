from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
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
    
    
@router.post("/submit-open-ended-quiz")
def submit_open_ended_quiz(
    payload: SubmitQuizRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    quiz = db.query(Quiz).filter_by(id=payload.quiz_id).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")

    correct_count = 0
    user_answer_objs = []

    for ans in payload.answers:
        question = db.query(Question).filter_by(id=ans.question_id).first()
        if not question or question.question_type_id != 2:  # 2: Open-ended
            continue

        expected_answer = question.open_ended_answer.strip().lower()
        user_answer = (ans.written_answer or "").strip().lower()

        is_correct = expected_answer == user_answer
        if is_correct:
            correct_count += 1

        user_answer_objs.append(UserAnswer(
            question_id=question.id,
            user_answer=ans.written_answer,
            is_correct=is_correct
        ))

    total_questions = len(user_answer_objs)
    score = round(correct_count / total_questions, 2) if total_questions else 0

    # Sonuçları kaydet
    result = UserQuizResult(
        user_id=current_user.id,
        quiz_id=quiz.id,
        skill_id=quiz.skill_id,
        score=score,
        correct_count=correct_count,
        total_questions=total_questions
    )
    db.add(result)
    db.commit()
    db.refresh(result)

    for ua in user_answer_objs:
        ua.result_id = result.id
        db.add(ua)

    db.commit()

    return {
        "result_id": result.id,
        "score": score,
        "correct_count": correct_count,
        "total_questions": total_questions
    }
