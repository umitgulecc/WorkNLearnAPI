# User veritabanı tablosu
from sqlalchemy.orm import relationship
from sqlalchemy import Column, ForeignKey, Integer, String, TIMESTAMP
from app.database import Base
import datetime
from app.models.level import Level
from app.models.role import Role
from app.models.department import Department
class User(Base):
    __tablename__ = "users"  # Veritabanında tablo adı

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)
    full_name = Column(String)
    created_at = Column(TIMESTAMP, default=datetime.datetime.utcnow)
    level_id = Column(Integer, ForeignKey(Level.id))  # ✅ Bunu eklemeyi unutma
    role_id = Column(Integer, ForeignKey(Role.id))
    department_id = Column(Integer, ForeignKey(Department.id))
    
    skill_scores = relationship("UserSkillScore", back_populates="user") # kullanıcının tüm SLWR skorlarına hızlı erişim
    role = relationship("Role", back_populates="users")
    department = relationship("Department", back_populates="users")
    quizzes = relationship("Quiz", back_populates="owner_user")

    def __repr__(self):
        return f"<User id={self.id} email={self.email} level_id={self.level_id} role_id={self.role_id} department_id={self.department_id}>"


