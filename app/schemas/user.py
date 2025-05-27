# User Tablosu Pydantic şema


from pydantic import BaseModel, EmailStr

# Kullanıcı kayıt formu şeması
class UserCreate(BaseModel):
    email: EmailStr
    full_name: str
    password: str
    role_id: int | None = None  # Rol ID'si opsiyonel, yönetici tarafından atanabilir
    department_id: int | None = None  # Departman ID'si opsiyonel, yönetici tarafından atanabilir

# Kullanıcı giriş formu
class UserLogin(BaseModel):
    email: EmailStr
    password: str
    department_id: int


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
        from_attributes = True  # eski adı orm_mode
        
        
class UserUpdate(BaseModel):
    full_name: str | None = None
    password: str | None = None
    
class UserBasicOut(BaseModel):
    id: int
    full_name: str
    email: str
    level_id: int

    class Config:
        from_attributes = True




class ForgotPasswordRequest(BaseModel):
    email: EmailStr

class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str
