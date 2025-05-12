from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.database import Base  # veya direkt sqlalchemy.declarative_base() kullanıyorsan ona göre
from app.models.skill import Skill
from app.models.level import Level
from app.models.quiz_type import QuizType  # QuizType modelini ekle

class Quiz(Base):
    __tablename__ = "quizzes"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(Text)
    skill_id = Column(Integer, ForeignKey(Skill.id))
    level_id = Column(Integer, ForeignKey(Level.id))
    is_placement_test = Column(Boolean, default=False)
    quiz_type_id = Column(Integer, ForeignKey(QuizType.id), nullable=False)
    
    quiz_type = relationship("QuizType", back_populates="quizzes")
    questions = relationship("Question", backref="quiz")


    def __repr__(self):
        return f"<Quiz id={self.id} title='{self.title}' skill_id={self.skill_id} type_id={self.quiz_type_id}>"
