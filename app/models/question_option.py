from sqlalchemy import Column, Integer, Boolean, ForeignKey, Text
from app.database import Base 
from app.models.question import Question


class QuestionOption(Base):
    __tablename__ = "question_options"
    id = Column(Integer, primary_key=True)
    question_id = Column(Integer, ForeignKey(Question.id))
    option_text = Column(Text, nullable=False)
    is_correct = Column(Boolean, default=False)