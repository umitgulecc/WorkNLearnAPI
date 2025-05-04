# User veritabanı tablosu
from sqlalchemy.orm import relationship
from sqlalchemy import Column, ForeignKey, Integer, String, TIMESTAMP
from app.database import Base
import datetime
from app.models.level import Level

class User(Base):
    __tablename__ = "users"  # Veritabanında tablo adı

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)
    full_name = Column(String)
    created_at = Column(TIMESTAMP, default=datetime.datetime.utcnow)
    level_id = Column(Integer, ForeignKey(Level.id))  # ✅ Bunu eklemeyi unutma
    skill_scores = relationship("UserSkillScore", back_populates="user") # kullanıcının tüm SLWR skorlarına hızlı erişim

