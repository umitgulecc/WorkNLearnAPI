from sqlalchemy import Column, Integer, Boolean, ForeignKey, Text
from app.database import Base
from app.models.question import Question
from app.models.user_quiz_result import UserQuizResult  
from sqlalchemy.orm import relationship

class UserAnswer(Base):
    __tablename__ = "user_answers"
    id = Column(Integer, primary_key=True)
    result_id = Column(Integer, ForeignKey(UserQuizResult.id), nullable=False)
    question_id = Column(Integer, ForeignKey(Question.id), nullable=False)
    user_answer = Column(Text, nullable=True)# Açık uçlu cevabı buraya yazarız
    selected_option_id = Column(Integer, ForeignKey("question_options.id"), nullable=True)
    is_correct = Column(Boolean, default=False)
    
    selected_option = relationship("QuestionOption")
