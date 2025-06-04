from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session
from app.models.quiz import Quiz
from app.models.question import Question
from app.models.question_option import QuestionOption
from app.models.quiz_type import QuizType
from app.models.skill import Skill
from app.models.topic import Topic
from app.models.question_type import QuestionType
from app.models.user import User
from app.models.quiz_type import QuizType
from app.models.question import Question
from app.models.question_option import QuestionOption
from app.models.topic import Topic
from app.models.question_type import QuestionType
from app.models.user import User
from sqlalchemy.orm import Session


def get_user_weak_topics(db: Session, user_id: int, limit: int = 3):
    from app.models.user_topic_stat import UserTopicStat
    return (
        db.query(UserTopicStat)
        .filter(UserTopicStat.user_id == user_id)
        .order_by(UserTopicStat.wrong_count.desc())
        .limit(limit)
        .all()
    )

# Dummy GPT fonksiyonu: bu kısmı önceden GPT ile entegreydi. Maliyetten ötürü fonksiyonumuzu değiştirdik.
def generate_questions_with_gpt(topics: list[Topic]):
    return [
        {
            "content": f"What is {topic.name} in a business context?",
            "question_type": "Multiple Choice",
            "options": [
                {"text": "Option A", "is_correct": False},
                {"text": "Option B", "is_correct": True},
                {"text": "Option C", "is_correct": False},
                {"text": "Option D", "is_correct": False}
            ],
            "topic_id": topic.id,
            "explanation": "Because X is commonly used in business contexts as..."

        }
        for topic in topics
    ]

#Quiz ve sorularını veritabanına kaydet
def create_personalized_quiz(db: Session, user_id: int):
    weak_stats = get_user_weak_topics(db, user_id)
    if not weak_stats:
        return None

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Kullanıcı bulunamadı.")

    topics = db.query(Topic).filter(Topic.id.in_([ws.topic_id for ws in weak_stats])).all()
    questions_data = generate_questions_with_gpt(topics)

    quiz_type = db.query(QuizType).filter(QuizType.name == "GPT Destekli Geliştirme Testleri").first()
    if not quiz_type:
        raise HTTPException(status_code=400, detail="GPT Destekli quiz türü tanımlı değil.")

    new_quiz = Quiz(
        title="GPT Destekli Kişisel Quiz",
        description="Zayıf olduğunuz konulara göre oluşturulmuştur.",
        skill_id=user.skill_scores[0].skill_id if user.skill_scores else 1,
        level_id=user.level_id,
        is_placement_test=False,
        quiz_type_id=quiz_type.id,
        is_personalized=True,
        owner_user_id=user.id,
        
    )
    db.add(new_quiz)
    db.commit()
    db.refresh(new_quiz)

    question_type = db.query(QuestionType).filter(QuestionType.id == 1).first()

    for q in questions_data:
        question = Question(
            quiz_id=new_quiz.id,
            content=q["content"],
            topic_id=q["topic_id"],
            question_type_id=question_type.id,
            explanation=q.get("explanation", "GPT tarafından otomatik oluşturulmuştur.")

        )
        db.add(question)
        db.commit()
        db.refresh(question)

        for opt in q["options"]:
            db.add(QuestionOption(
                question_id=question.id,
                option_text=opt["text"],
                is_correct=opt["is_correct"]
            ))

    db.commit()
    return new_quiz


# Kullanıcıya özel yerleştirme testi oluşturma
def create_personalized_placement_quiz(db: Session, user) -> Quiz:
    weak_stats = db.query(Topic).limit(1).all()#Test için geçici olarak bir tane topic alıyoruz
    if not weak_stats:
        return None

    topics = db.query(Topic).filter(Topic.id.in_([t.id for t in weak_stats])).all()
    questions_data = generate_questions_with_gpt(topics)

    quiz_type_id = db.query(QuizType).filter(QuizType.name == "GPT Destekli Yerleştirme Testleri").first().id
    question_type = db.query(QuestionType).filter(QuestionType.id == 1).first()

    new_quiz = Quiz(
        title="Kişisel Yerleştirme Testi (GPT)",
        description="GPT tarafından zayıf olduğunuz konulara göre oluşturulmuştur.",
        skill_id=user.skill_id,
        level_id=user.level_id,
        is_placement_test=True,
        quiz_type_id=quiz_type_id,
        is_personalized=True,
        owner_user_id=user.id
    )
    db.add(new_quiz)
    db.commit()
    db.refresh(new_quiz)

    for q in questions_data:
        question = Question(
            quiz_id=new_quiz.id,
            content=q["content"],
            topic_id=q["topic_id"],
            question_type_id=question_type.id
        )
        db.add(question)
        db.flush() 


        for opt in q["options"]:
            db.add(QuestionOption(
                question_id=question.id,
                option_text=opt["text"],
                is_correct=opt["is_correct"]
            ))

    db.commit()
    return new_quiz