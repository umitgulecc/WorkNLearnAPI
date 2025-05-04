from sqlalchemy.orm import Session, joinedload
from app.models.quiz import Quiz, Question
from sqlalchemy.orm import Session

def get_quizzes_by_user_level(db: Session, user_level_id: int):
    return db.query(Quiz).filter(
        (Quiz.level_id <= user_level_id) | (Quiz.is_placement_test == True)
    ).all()


def get_quiz_with_questions(db: Session, quiz_id: int):
    return db.query(Quiz).options(
        joinedload(Quiz.questions).joinedload(Question.options)  # ✅ DİKKAT: string değil!
    ).filter(Quiz.id == quiz_id).first()