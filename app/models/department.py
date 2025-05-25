from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Department(Base):
    __tablename__ = "departments"
    
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    manager_id = Column(Integer, ForeignKey("users.id"))

    # ❗ foreign_keys belirtiyoruz
    manager = relationship("User", foreign_keys=[manager_id], backref="managed_department")

    # Ters ilişki için kullanıcıları (departmana ait) listelemek istersen:
    users = relationship("User", back_populates="department", foreign_keys="User.department_id")
