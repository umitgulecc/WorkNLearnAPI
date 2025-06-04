from __future__ import annotations
from sqlalchemy.orm import relationship
from sqlalchemy import Column, ForeignKey, Integer, String, TIMESTAMP
from app.database import Base
from app.models.level import Level
from app.models.role import Role
import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)
    full_name = Column(String)
    created_at = Column(TIMESTAMP, default=datetime.datetime.utcnow)
    level_id = Column(Integer, ForeignKey(Level.id))
    role_id = Column(Integer, ForeignKey(Role.id))
    department_id = Column(Integer, ForeignKey("departments.id"))
    
    
    skill_scores = relationship("UserSkillScore", back_populates="user")
    role = relationship("Role", back_populates="users")
    quizzes = relationship("Quiz", back_populates="owner_user")
    department = relationship("Department", back_populates="users", foreign_keys=[department_id])
    quiz_results = relationship("UserQuizResult", back_populates="user", cascade="all, delete")

    def __repr__(self):
        return f"<User id={self.id} email={self.email} level_id={self.role_id} role_id={self.role_id} department_id={self.department_id}>"
