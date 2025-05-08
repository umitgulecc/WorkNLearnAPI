from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.database import Base  # veya direkt sqlalchemy.declarative_base() kullanıyorsan ona göre
from app.models.skill import Skill
from app.models.level import Level


class Quiz(Base):
    __tablename__ = "quizzes"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(Text)
    skill_id = Column(Integer, ForeignKey(Skill.id))
    level_id = Column(Integer, ForeignKey(Level.id))
    is_placement_test = Column(Boolean, default=False)

    questions = relationship("Question", backref="quiz")




