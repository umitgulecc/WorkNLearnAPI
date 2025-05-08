from sqlalchemy import Column, Integer, String
from app.database import Base

class QuestionType(Base):
    __tablename__ = "question_types"

    id = Column(Integer, primary_key=True, index=True)
    type_name = Column(String, unique=True, nullable=False)
