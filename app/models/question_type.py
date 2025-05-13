from sqlalchemy import Column, Integer, String
from app.database import Base
from sqlalchemy.orm import relationship
class QuestionType(Base):
    __tablename__ = "question_types"

    id = Column(Integer, primary_key=True, index=True)
    type_name = Column(String, unique=True, nullable=False)

    questions = relationship("Question", back_populates="question_type")
    
    def __repr__(self):
        return f"<QuestionType id={self.id} name='{self.type_name}'>"