from app.database import Base
from app.models.question_type import QuestionType
from app.models.quiz import Quiz
from app.models.topic import Topic
from sqlalchemy import Column, Integer, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.models.reading_passages import ReadingPassage  # ReadingPassage modelini ekle
class Question(Base):
    __tablename__ = "questions"
    id = Column(Integer, primary_key=True)
    quiz_id = Column(Integer, ForeignKey(Quiz.id))
    content = Column(Text, nullable=False)
    explanation = Column(Text)
    topic_id = Column(Integer, ForeignKey(Topic.id))
    question_type_id = Column(Integer, ForeignKey(QuestionType.id))  # Foreign key to question_types table
    
    open_ended_answer = Column(Text, nullable=True)  # ✅ Open-ended sorular için doğru cevap
    reading_passage_id = Column(Integer, ForeignKey(ReadingPassage.id, ondelete="SET NULL"), nullable=True)

    reading_passage = relationship("ReadingPassage", back_populates="questions")
    options = relationship("QuestionOption", backref="question", cascade="all, delete-orphan")
    question_type = relationship("QuestionType", back_populates="questions")
