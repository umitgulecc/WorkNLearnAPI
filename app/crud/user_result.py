from sqlalchemy.orm import Session, joinedload
from fastapi import HTTPException, logger
from datetime import datetime

from app.models.quiz import Quiz
from app.models.question import Question
from app.models.question_option import QuestionOption
from app.models.question_type import QuestionType
from app.models.user_quiz_result import UserQuizResult
from app.models.user_answer import UserAnswer
from app.models.user_skill_score import UserSkillScore
from app.schemas.user_result import UserAnswerIn


 
def update_user_skill_score(db: Session, user_id: int, skill_id: int, score: float):
    existing = db.query(UserSkillScore).filter_by(user_id=user_id, skill_id=skill_id).first()
    if existing:
        existing.total_score += score
        existing.updated_at = datetime.utcnow()
    else:
        new_score = UserSkillScore(
            user_id=user_id,
            skill_id=skill_id,
            total_score=score
        )
        db.add(new_score)
    db.commit()



# Bir kullanıcının çözdüğü bir quiz'e ait detaylı cevap incelemesini döner.
#     - Hangi soruya ne cevap verdi?
#     - Hangi seçenek doğruydu?
#     - Açıklamalar nedir?    
def get_quiz_review(db: Session, user_id: int, result_id: int):
    """
    Quiz çözümünden sonra kullanıcıya çözümleme ekranı göstermek için:
    - Kullanıcının seçtiği cevaplar
    - Doğru seçenekler
    - Açıklamalar
    - Soru tipi
    """
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

        reviewed_questions.append({
            "id": question.id,
            "content": question.content,
            "question_type": question.question_type.type_name,
            "explanation": question.explanation,
            "user_selected_option_id": selected.selected_option_id if selected else None,
            "options": [
                {
                    "id": opt.id,
                    "option_text": opt.option_text,
                    "is_correct": opt.is_correct
                } for opt in question.options
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
    
    
# Kullanıcının verdiği cevaplara göre:
#     - Her soru için doğru/yanlış kontrolü yapar
#     - Tüm cevapları structured şekilde listeler
#     - Toplam doğru sayısını döner    
def evaluate_answers(questions: list, answers: list[UserAnswerIn]) -> tuple[list[dict], int]:
    correct_count = 0
    evaluated_answers = []

    # Kullanıcının cevaplarını dict'e çeviriyoruz: question_id → cevap
    answers_dict = {a.question_id: a for a in answers}

    for q in questions:
        user_ans = answers_dict.get(q.id)
        if not user_ans:
            continue  # bu soru cevaplanmamış

        is_correct = False
        selected_option_id = getattr(user_ans, "selected_option_id", None)
        user_written_answer = getattr(user_ans, "written_answer", None)
        print(f"deneme:{q.question_type}")
        if q.question_type_id == 1:
            correct_option = next((opt for opt in q.options if opt.is_correct), None)
            if selected_option_id == correct_option.id:
                is_correct = True

        elif q.question_type_id == 2:
            # Şimdilik yazılı cevabı varsa doğru sayıyoruz (AI yoksa)
            is_correct = True if user_written_answer else False

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
    total_questions = len(evaluated_answers)
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


# Quiz ID'sine göre:
#    - İlgili quiz nesnesini
#    - İlişkili soruları ve her sorunun seçeneklerini birlikte getirir.
def get_quiz_and_questions(db, quiz_id: int):
    return (
        db.query(Quiz)
        .options(joinedload(Quiz.questions).joinedload(Question.options))
        .filter(Quiz.id == quiz_id)
        .first()
    )