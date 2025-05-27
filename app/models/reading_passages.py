from sqlalchemy import Column, Integer, Text
from sqlalchemy.orm import relationship
from app.database import Base  # varsayım: tüm modeller Base'den türetiliyor

class ReadingPassage(Base):
    __tablename__ = "reading_passages"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(Text)
    content = Column(Text)

    questions = relationship("Question", back_populates="reading_passage", cascade="all, delete")
