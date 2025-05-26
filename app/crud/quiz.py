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
    current_user_id: int,
    quiz_type_id=None,
    skill_id=None,
    level_id=None,
    exclude_solved_by_user_id: int | None = None  # 🔥 Burayı ekle
):
    query = db.query(Quiz).filter(
        ((Quiz.level_id <= user_level_id) | (Quiz.is_placement_test == True)) &
        (
            (Quiz.is_personalized == False) |
            ((Quiz.is_personalized == True) & (Quiz.owner_user_id == current_user_id))
        )
    )

    if quiz_type_id is not None:
        query = query.filter(Quiz.quiz_type_id == quiz_type_id)
    if skill_id is not None:
        query = query.filter(Quiz.skill_id == skill_id)
    if level_id is not None:
        query = query.filter(Quiz.level_id == level_id)

    # 🔒 Çözdüğü quizleri dışla
    if exclude_solved_by_user_id:
        from app.models.user_quiz_result import UserQuizResult
        solved_quiz_ids = db.query(UserQuizResult.quiz_id).filter(
            UserQuizResult.user_id == exclude_solved_by_user_id
        ).subquery()
        query = query.filter(~Quiz.id.in_(solved_quiz_ids))

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
    




def get_last_placement_result(db: Session, user_id: int) -> UserQuizResult | None:
    return (
        db.query(UserQuizResult)
        .join(Quiz, UserQuizResult.quiz_id == Quiz.id)
        .filter(UserQuizResult.user_id == user_id, Quiz.quiz_type_id == 1)
        .order_by(UserQuizResult.taken_at.desc())
        .first()
    )
