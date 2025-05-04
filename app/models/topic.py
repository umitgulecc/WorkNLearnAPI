
from sqlalchemy import Column, Integer, String
from app.database import Base

class Topic(Base):
    __tablename__ = "topics"  # Veritabanında tablo adı

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)