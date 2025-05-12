from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database import Base
from app.models.user import User  
from app.models.skill import Skill 
class UserSkillScore(Base):
    __tablename__ = "user_skill_scores"
    __table_args__ = (UniqueConstraint('user_id', 'skill_id', name='uq_user_skill'),)

    id = Column(Integer, primary_key=True)
    
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    skill_id = Column(Integer, ForeignKey(Skill.id), nullable=False)
    
    total_score = Column(Float, default=0)
    updated_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="skill_scores")
    skill = relationship("Skill")


    def __repr__(self):
        return f"<UserSkillScore user_id={self.user_id} skill_id={self.skill_id} score={self.total_score}>"
