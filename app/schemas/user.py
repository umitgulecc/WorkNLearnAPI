from typing import Optional
from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    full_name: str
    password: str
    role_id: int | None = None
    department_id: int | None = None 

class UserLogin(BaseModel):
    email: EmailStr
    password: str
    department_id: Optional[int] = None


class SkillScoreOut(BaseModel):
    skill_id: int
    skill_name: str
    total_score: float

class UserProfile(BaseModel):
    id: int
    full_name: str
    email: str
    level_id: int
    skill_scores: list[SkillScoreOut]

    class Config:
        from_attributes = True
        
        
class UserUpdate(BaseModel):
    full_name: str | None = None
    password: str | None = None
    
class UserBasicOut(BaseModel):
    id: int
    full_name: str
    email: str
    role_id: Optional[int] = None
    department_id: Optional[int] = None

    class Config:
        from_attributes = True




class ForgotPasswordRequest(BaseModel):
    email: EmailStr

class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str
