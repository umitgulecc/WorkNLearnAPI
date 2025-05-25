from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.quiz import Quiz
from app.models.question import Question
from app.models.question_option import QuestionOption
from app.models.quiz_type import QuizType
from app.models.skill import Skill
from app.models.topic import Topic
from app.models.question_type import QuestionType
from app.models.user import User

# 1️⃣ Zayıf konularını getir
def get_user_weak_topics(db: Session, user_id: int, limit: int = 3):
    from app.models.user_topic_stat import UserTopicStat
    return (
        db.query(UserTopicStat)
        .filter(UserTopicStat.user_id == user_id)
        .order_by(UserTopicStat.wrong_count.desc())
        .limit(limit)
        .all()
    )

# 2️⃣ Dummy GPT fonksiyonu: bu kısmı sonra OpenAI API ile güncelleriz
def generate_questions_with_gpt(topics: list[Topic]):
    # Örnek dummy veri
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

# 3️⃣ Quiz ve sorularını veritabanına kaydet
def create_personalized_quiz(db: Session, user_id: int):
    # Kullanıcının zayıf olduğu konuları al
    weak_stats = get_user_weak_topics(db, user_id)
    if not weak_stats:
        return None

    # Kullanıcı nesnesi alınmalı çünkü level ve skill id'ye ihtiyacımız var
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Kullanıcı bulunamadı.")

    # Zayıf olunan konulara göre GPT'den sorular üret
    topics = db.query(Topic).filter(Topic.id.in_([ws.topic_id for ws in weak_stats])).all()
    questions_data = generate_questions_with_gpt(topics)

    # Quiz türünü al
    quiz_type = db.query(QuizType).filter(QuizType.name == "GPT Destekli Geliştirme Testleri").first()
    if not quiz_type:
        raise HTTPException(status_code=400, detail="GPT Destekli quiz türü tanımlı değil.")

    # Yeni quiz oluştur
    new_quiz = Quiz(
        title="GPT Destekli Kişisel Quiz",
        description="Zayıf olduğunuz konulara göre oluşturulmuştur.",
        skill_id=user.skill_scores[0].skill_id if user.skill_scores else 1,  # varsayılan skill
        level_id=user.role_id,
        is_placement_test=False,
        quiz_type_id=quiz_type.id,
        is_personalized=True,
        owner_user_id=user.id,
        
    )
    db.add(new_quiz)
    db.commit()
    db.refresh(new_quiz)

    # Soru tipi (varsayılan olarak multiple choice kullanıyoruz)
    question_type = db.query(QuestionType).filter(QuestionType.id == 1).first()

    for q in questions_data:
        question = Question(
            quiz_id=new_quiz.id,
            content=q["content"],
            topic_id=q["topic_id"],
            question_type_id=question_type.id,
            explanation=q.get("explanation", "GPT tarafından otomatik oluşturulmuştur.")  # ✅ burada

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
