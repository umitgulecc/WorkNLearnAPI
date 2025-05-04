# User Tablosu Pydantic şema


from pydantic import BaseModel, EmailStr

# Kullanıcı kayıt formu şeması
class UserCreate(BaseModel):
    email: EmailStr
    full_name: str
    password: str

# Kullanıcı giriş formu
class UserLogin(BaseModel):
    email: EmailStr
    password: str

# Kullanıcı bilgisi döndürme şeması (şifre hariç)
class UserResponse(BaseModel):
    id: int
    email: EmailStr
    full_name: str

    class Config:
        orm_mode = True  # SQLAlchemy objesini JSON'a çevirmek için
