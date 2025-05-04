from sqlalchemy import Column, DateTime, Float, Integer, String, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.database import Base  # veya direkt sqlalchemy.declarative_base() kullanıyorsan ona göre

class UserQuizResult(Base):
    __tablename__ = "user_quiz_results"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    quiz_id = Column(Integer, ForeignKey("quizzes.id"))
    skill_id = Column(Integer, ForeignKey("skills.id"))
    score = Column(Float)
    correct_count = Column(Integer)
    total_questions = Column(Integer)
    taken_at = Column(DateTime)

class UserAnswer(Base):
    __tablename__ = "user_answers"
    id = Column(Integer, primary_key=True)
    result_id = Column(Integer, ForeignKey("user_quiz_results.id"), nullable=False)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    user_answer = Column(Text, nullable=True)# Açık uçlu cevabı buraya yazarız
    selected_option_id = Column(Integer, ForeignKey("question_options.id"), nullable=True)
    is_correct = Column(Boolean, default=False)
    
class UserTopicStats(Base):
    __tablename__ = "user_topic_stats"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    topic_id = Column(Integer, ForeignKey("topics.id"), nullable=False)
    wrong_count = Column(Integer, default=0)
