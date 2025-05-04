from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database import Base  # Projenin yapısına göre Base import’un doğru olduğuna emin ol

class UserSkillScore(Base):
    __tablename__ = "user_skill_scores"
    __table_args__ = (UniqueConstraint('user_id', 'skill_id', name='uq_user_skill'),)

    id = Column(Integer, primary_key=True)
    
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    skill_id = Column(Integer, ForeignKey("skills.id"), nullable=False)
    
    total_score = Column(Float, default=0)
    updated_at = Column(DateTime, default=datetime.utcnow)

    # İsteğe bağlı: ilişkiler
    user = relationship("User", back_populates="skill_scores")
    skill = relationship("Skill")
