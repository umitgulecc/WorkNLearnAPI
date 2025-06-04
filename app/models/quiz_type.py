from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base


class QuizType(Base):
    __tablename__ = "quiz_types"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    quizzes = relationship("Quiz", back_populates="quiz_type")


    def __repr__(self):
        return f"<QuizType id={self.id} name='{self.name}'>"
