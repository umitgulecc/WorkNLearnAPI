from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import datetime

from app.models.quiz import Quiz
from app.models.question import Question
from app.models.question_option import QuestionOption
from app.models.user_answer import UserAnswer
from app.models.user_quiz_result import UserQuizResult
from app.schemas.submission import UserAnswerIn




# Kullanıcının verdiği cevaplara göre:
#     - Her soru için doğru/yanlış kontrolü yapar
#     - Tüm cevapları structured şekilde listeler
#     - Toplam doğru sayısını döner    
def evaluate_answers(questions: list, answers: list[UserAnswerIn]) -> tuple[list[dict], int]:
    correct_count = 0
    evaluated_answers = []

    answers_dict = {a.question_id: a for a in answers}

    for q in questions:
        user_ans = answers_dict.get(q.id)
        if not user_ans:
            continue

        is_correct = False
        selected_option_id = getattr(user_ans, "selected_option_id", None)
        user_written_answer = (getattr(user_ans, "written_answer", "") or "").strip().lower()

        if q.question_type_id == 1:  # Çoktan seçmeli
            correct_option = next((opt for opt in q.options if opt.is_correct), None)
            if correct_option and selected_option_id == correct_option.id:
                is_correct = True

        elif q.question_type_id == 2:  # Açık uçlu
            expected = (q.open_ended_answer or "").strip().lower()
            is_correct = expected == user_written_answer

        if is_correct:
            correct_count += 1

        evaluated_answers.append({
            "question_id": q.id,
            "selected_option_id": selected_option_id,
            "user_answer": user_written_answer,
            "is_correct": is_correct
        })

    return evaluated_answers, correct_count




# Quiz değerlendirmesi sonucunu veritabanına kaydeder.
#     - UserQuizResult oluşturur
#     - UserAnswer kayıtlarını toplu şekilde ekler
#     - Skor hesaplayıp geri döner
def save_user_quiz_result(db, user_id, quiz, evaluated_answers, correct_count):
    total_questions = len(quiz.questions)  # 🔧 Burayı düzelttik
    score = round(correct_count / total_questions, 2) if total_questions else 0

    result = UserQuizResult(
        user_id=user_id,
        quiz_id=quiz.id,
        skill_id=quiz.skill_id,
        correct_count=correct_count,
        total_questions=total_questions,
        score=score,
        taken_at=datetime.utcnow()
    )
    db.add(result)
    db.commit()
    db.refresh(result)

    user_answer_objs = [
        UserAnswer(
            result_id=result.id,
            question_id=ans["question_id"],
            selected_option_id=ans["selected_option_id"],
            user_answer=ans["user_answer"],
            is_correct=ans["is_correct"]
        ) for ans in evaluated_answers
    ]
    db.bulk_save_objects(user_answer_objs)
    db.commit()

    return result, score
