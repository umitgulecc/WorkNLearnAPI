from app.database import Base
from app.models.question_type import QuestionType
from app.models.quiz import Quiz
from app.models.topic import Topic
from sqlalchemy import Column, Integer, ForeignKey, Text
from sqlalchemy.orm import relationship
class Question(Base):
    __tablename__ = "questions"
    id = Column(Integer, primary_key=True)
    quiz_id = Column(Integer, ForeignKey(Quiz.id))
    content = Column(Text, nullable=False)
    explanation = Column(Text)
    topic_id = Column(Integer, ForeignKey(Topic.id))
    question_type_id = Column(Integer, ForeignKey(QuestionType.id))  # Foreign key to question_types table

    options = relationship("QuestionOption", backref="question")