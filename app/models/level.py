# levels veritabanı tablosu

from sqlalchemy import Column, Integer, String
from app.database import Base


class Level(Base):
    __tablename__ = "levels"  # Veritabanında tablo adı

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)