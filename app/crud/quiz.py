from sqlalchemy.orm import Session, joinedload
from app.models.quiz import Quiz
from app.models.question import Question
from sqlalchemy.orm import Session
from app.models.user_quiz_result import UserQuizResult


# Kullanıcının seviyesine ve opsiyonel filtrelere göre quiz listesi döner.
# - Seviye ≤ user_level_id olan quizler
# - Veya seviye belirleyici (placement) quizler
# - Opsiyonel filtreler: quiz_type_id, skill_id, level_id
def get_quizzes_by_filters(
    db: Session,
    user_level_id: int,
    quiz_type_id: int | None = None,
    skill_id: int | None = None,
    level_id: int | None = None,
    exclude_solved_by_user_id: int | None = None  # ✅ yeni parametre
):
    query = db.query(Quiz)

    if exclude_solved_by_user_id is not None:
        solved_ids = db.query(UserQuizResult.quiz_id).filter_by(user_id=exclude_solved_by_user_id)
        query = query.filter(Quiz.id.notin_(solved_ids))

    if quiz_type_id:
        query = query.filter(Quiz.quiz_type_id == quiz_type_id)
    if skill_id:
        query = query.filter(Quiz.skill_id == skill_id)
    if level_id:
        query = query.filter(Quiz.level_id == level_id)
    else:
        query = query.filter(Quiz.level_id == user_level_id)

    return query.all()





# Quiz ID’sine göre quiz nesnesini, içindeki soruları ve her sorunun seçeneklerini getirir.
#     - joinedload ile ilişkiler performanslı şekilde alınır
def get_quiz_with_questions(db: Session, quiz_id: int):
    return db.query(Quiz).options(
        joinedload(Quiz.questions)
        .joinedload(Question.options),
        joinedload(Quiz.questions)
        .joinedload(Question.question_type) 
    ).filter(Quiz.id == quiz_id).first()
    
