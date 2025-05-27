from sqlalchemy.orm import Session, joinedload
from fastapi import HTTPException

from app.models.quiz import Quiz
from app.models.question import Question
from app.models.user_quiz_result import UserQuizResult
from app.models.user_answer import UserAnswer
from app.schemas.review import QuizReview, ReviewedQuestion, ReviewedOption




# Bir kullanıcının çözdüğü bir quiz'e ait detaylı cevap incelemesini döner.
#     - Hangi soruya ne cevap verdi?
#     - Hangi seçenek doğruydu?
#     - Açıklamalar nedir?    
def get_quiz_review(db: Session, user_id: int, result_id: int) -> QuizReview:
    result = db.query(UserQuizResult).filter_by(id=result_id, user_id=user_id).first()
    if not result:
        raise HTTPException(status_code=404, detail="Result not found")

    quiz = db.query(Quiz).filter_by(id=result.quiz_id).first()

    questions = (
        db.query(Question)
        .options(joinedload(Question.question_type), joinedload(Question.options))
        .filter_by(quiz_id=quiz.id)
        .all()
    )

    answers = db.query(UserAnswer).filter_by(result_id=result.id).all()
    answer_map = {a.question_id: a for a in answers}

    reviewed_questions = []

    for question in questions:
        selected = answer_map.get(question.id)

        if question.question_type_id == 1:  # Multiple Choice
            reviewed_questions.append(ReviewedQuestion(
                id=question.id,
                content=question.content,
                question_type=question.question_type.type_name,
                explanation=question.explanation or "GPT tarafından açıklama verilmemiştir.",
                user_selected_option_id=selected.selected_option_id if selected else None,
                options=[
                    ReviewedOption(
                        id=opt.id,
                        option_text=opt.option_text,
                        is_correct=opt.is_correct
                    ) for opt in question.options
                ]
            ))

        elif question.question_type_id == 2:  # Open-ended
            reviewed_questions.append(ReviewedQuestion(
                id=question.id,
                content=question.content,
                question_type=question.question_type.type_name,
                explanation=question.explanation or "GPT tarafından açıklama verilmemiştir.",
                user_answer=selected.user_answer if selected else None,
                expected_answer=question.open_ended_answer,
                is_correct=selected.is_correct if selected else None,
                options=[]  # Open-ended için opsiyon yok
            ))

    return QuizReview(
        quiz_id=quiz.id,
        quiz_title=quiz.title,
        taken_at=result.taken_at,
        score=result.score,
        correct_count=result.correct_count,
        total_questions=result.total_questions,
        questions=reviewed_questions,    )
