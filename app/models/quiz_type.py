# levels veritabanı tablosu

from sqlalchemy import Column, Integer, String
from app.database import Base


class QuizType(Base):
    __tablename__ = "quiz_types"  # Veritabanında tablo adı

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)