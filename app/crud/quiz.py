from sqlalchemy.orm import Session, joinedload
from app.models.quiz import Quiz
from app.models.question import Question
from sqlalchemy.orm import Session



# Kullanıcının seviyesine ve opsiyonel filtrelere göre quiz listesi döner.
# - Seviye ≤ user_level_id olan quizler
# - Veya seviye belirleyici (placement) quizler
# - Opsiyonel filtreler: quiz_type_id, skill_id, level_id
def get_quizzes_by_filters(db: Session, user_level_id: int, quiz_type_id=None, skill_id=None, level_id=None):
    query = db.query(Quiz).filter(
        (Quiz.level_id <= user_level_id) | (Quiz.is_placement_test == True)
    )

    if quiz_type_id is not None:
        query = query.filter(Quiz.quiz_type_id == quiz_type_id)

    if skill_id is not None:
        query = query.filter(Quiz.skill_id == skill_id)

    if level_id is not None:
        query = query.filter(Quiz.level_id == level_id)

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
    


def get_quizzes_by_filters(db: Session, user_level_id: int, quiz_type_id=None, skill_id=None, level_id=None):
    query = db.query(Quiz).filter(
        (Quiz.level_id <= user_level_id) | (Quiz.is_placement_test == True)
    )

    if quiz_type_id:
        query = query.filter(Quiz.quiz_type_id == quiz_type_id)

    if skill_id:
        query = query.filter(Quiz.skill_id == skill_id)

    if level_id:
        query = query.filter(Quiz.level_id == level_id)

    return query.all()
