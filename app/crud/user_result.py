from sqlalchemy.orm import Session
from app.models.question_type import QuestionType
from app.models.quiz import Quiz
from app.models.question import Question
from app.models.question_option import QuestionOption
from app.models.user_quiz_result import UserQuizResult
from app.models.user_answer import UserAnswer
from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import datetime
from app.schemas.user_result import UserAnswerIn

def evaluate_and_save_quiz(db: Session, user_id: int, quiz_id: int, answers: list[UserAnswerIn]):
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if not quiz:
        raise HTTPException(404, "Quiz not found")

    correct_count = 0
    user_answer_objects = []

    for ans in answers:
        question = db.query(Question).filter(Question.id == ans.question_id).first()
        if not question:
            continue

        is_correct = False  # default

        if question.question_type_id == 1:
            if not ans.selected_option_id:
                raise HTTPException(400, "Missing selected_option_id for multiple choice question")
            selected_option = db.query(QuestionOption).filter(
                QuestionOption.id == ans.selected_option_id,
                QuestionOption.question_id == ans.question_id
            ).first()
            if not selected_option:
                raise HTTPException(400, "Invalid selected option")

            is_correct = selected_option.is_correct
            if is_correct:
                correct_count += 1

            user_answer_objects.append(UserAnswer(
                question_id=question.id,
                selected_option_id=ans.selected_option_id,
                is_correct=is_correct
            ))

        elif question.question_type_id == 2:
            if not ans.written_answer:
                raise HTTPException(400, "Missing written_answer for open-ended question")

            user_answer_objects.append(UserAnswer(
                question_id=question.id,
                user_answer=ans.written_answer,
                is_correct=False  # open-ended için sonra değerlendirme yapılabilir
            ))

    total_questions = len(answers)
    score = correct_count / total_questions if total_questions > 0 else 0

    result = UserQuizResult(
        user_id=user_id,
        quiz_id=quiz_id,
        skill_id=quiz.skill_id,
        score=score,
        correct_count=correct_count,
        total_questions=total_questions,
        taken_at=datetime.utcnow()
    )
    db.add(result)
    db.commit()
    db.refresh(result)

    for ua in user_answer_objects:
        ua.result_id = result.id
        db.add(ua)

    db.commit()
    return {
        "result_id": result.id,
        "score": score,
        "correct_count": correct_count,
        "total_questions": total_questions
    }
 
    
    
def get_quiz_review(db: Session, user_id: int, result_id: int):
    result = db.query(UserQuizResult).filter_by(id=result_id, user_id=user_id).first()
    if not result:
        raise HTTPException(status_code=404, detail="Result not found")

    quiz = db.query(Quiz).filter_by(id=result.quiz_id).first()
    questions = db.query(Question).filter_by(quiz_id=quiz.id).all()

    # Kullanıcının verdiği cevaplar
    answers = db.query(UserAnswer).filter_by(result_id=result.id).all()
    answer_map = {a.question_id: a for a in answers}

    reviewed_questions = []

    for question in questions:
        options = db.query(QuestionOption).filter_by(question_id=question.id).all()
        selected = answer_map.get(question.id)
        
        question_type = db.query(QuestionType).filter(QuestionType.id == question.question_type_id).first()
        reviewed_questions.append({
            "id": question.id,
            "content": question.content,
            "question_type": question_type.type_name,
            "explanation": question.explanation,
            "user_selected_option_id": selected.selected_option_id if selected else None,
            "options": [
                {
                    "id": opt.id,
                    "option_text": opt.option_text,
                    "is_correct": opt.is_correct
                } for opt in options
            ]
        })

    return {
        "quiz_id": quiz.id,
        "quiz_title": quiz.title,
        "taken_at": result.taken_at,
        "score": result.score,
        "correct_count": result.correct_count,
        "total_questions": result.total_questions,
        "questions": reviewed_questions
    }