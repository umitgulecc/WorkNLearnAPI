from sqlalchemy import Column, DateTime, Float, Integer, String, Boolean, ForeignKey, Text
from app.database import Base  # veya direkt sqlalchemy.declarative_base() kullanıyorsan ona göre
from app.models.quiz import Quiz
from app.models.skill import Skill
from app.models.user import User 
from sqlalchemy.orm import relationship
class UserQuizResult(Base):
    __tablename__ = "user_quiz_results"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    quiz_id = Column(Integer, ForeignKey(Quiz.id))
    skill_id = Column(Integer, ForeignKey(Skill.id))
    score = Column(Float)
    correct_count = Column(Integer)
    total_questions = Column(Integer)
    taken_at = Column(DateTime)

    answers = relationship("UserAnswer", backref="result", cascade="all, delete-orphan")  # ✅ BURASI EKLENECEK
    user = relationship("User", back_populates="quiz_results", passive_deletes=True)
    quiz = relationship("Quiz", back_populates="results")
    
    def __repr__(self):
        return f"<UserQuizResult id={self.id} user_id={self.user_id} quiz_id={self.quiz_id} score={self.score}>"
