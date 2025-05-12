import datetime
from sqlalchemy.orm import Session
from app.database import get_db
from app.auth.auth import get_current_user
from fastapi import APIRouter, Depends, HTTPException
from app.schemas.user_result import SubmitQuizRequest
from app.crud.user_result import get_quiz_review
from app.schemas.user_result import QuizReview
from app.models.user_skill_score import UserSkillScore
from app.models.quiz import Quiz
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.user_result import SubmitQuizRequest
from app.models.user import User
from app.crud.user_result import (
    get_quiz_and_questions,
    evaluate_answers,
    save_user_quiz_result,
)
from app.crud.user_result import update_user_skill_score

router = APIRouter()

router = APIRouter()
@router.post("/submit-quiz")
def submit_quiz(
    payload: SubmitQuizRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    quiz = get_quiz_and_questions(db, payload.quiz_id)

    if not quiz:
        raise HTTPException(404, "Quiz not found")

    evaluated_answers, correct_count = evaluate_answers(quiz.questions, payload.answers)
    result, score = save_user_quiz_result(db, current_user.id, quiz, evaluated_answers, correct_count)
    update_user_skill_score(db=db, user_id=current_user.id, skill_id=quiz.skill_id, score=score)

    return {
        "detail": "Quiz submitted successfully",
        "score": score,
        "result_id": result.id
    }
    
      
@router.get("/review-quiz/{result_id}", response_model=QuizReview)
def review_quiz(
    result_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return get_quiz_review(db, current_user.id, result_id)



