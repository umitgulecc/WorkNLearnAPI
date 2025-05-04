from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.database import Base  # veya direkt sqlalchemy.declarative_base() kullanıyorsan ona göre
from app.models.skill import Skill
from app.models.level import Level
from app.models.topic import Topic


class Quiz(Base):
    __tablename__ = "quizzes"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(Text)
    skill_id = Column(Integer, ForeignKey(Skill.id))
    level_id = Column(Integer, ForeignKey(Level.id))
    is_placement_test = Column(Boolean, default=False)

    questions = relationship("Question", backref="quiz")


class Question(Base):
    __tablename__ = "questions"
    id = Column(Integer, primary_key=True)
    quiz_id = Column(Integer, ForeignKey(Quiz.id))
    content = Column(Text, nullable=False)
    explanation = Column(Text)
    topic_id = Column(Integer, ForeignKey(Topic.id))
    question_type = Column(String)

    options = relationship("QuestionOption", backref="question")


class QuestionOption(Base):
    __tablename__ = "question_options"
    id = Column(Integer, primary_key=True)
    question_id = Column(Integer, ForeignKey(Question.id))
    option_text = Column(Text, nullable=False)
    is_correct = Column(Boolean, default=False)

