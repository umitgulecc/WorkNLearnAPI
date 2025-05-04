from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app.auth.auth import get_current_user
from app.models.user import User
from app.database import SessionLocal
from app.schemas.user import UserCreate, UserLogin, UserResponse
from app.crud.user import create_user, get_user_by_email
from app.utils import verify_password
from app.auth.auth import create_access_token

router = APIRouter()  # <-- BU SATIR ÇOK ÖNEMLİ

# Veritabanı bağlantısı
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    if get_user_by_email(db, user.email):
        raise HTTPException(status_code=400, detail="❌ Bu e-posta adresi zaten kayıtlı.")
    
    created_user = create_user(db, user.email, user.full_name, user.password)
    
    return {
        "message": f"✅ Kayıt başarılı. Hoş geldiniz, {created_user.full_name}!",
        "user": {
            "id": created_user.id,
            "email": created_user.email,
            "full_name": created_user.full_name
        }
    }

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, form_data.username)  # 👈 username yerine e-posta geliyor
    if not db_user or not verify_password(form_data.password, db_user.password_hash):
        raise HTTPException(status_code=401, detail="E-posta veya şifre hatalı.")
    
    token = create_access_token(data={"sub": db_user.email})
    return {
        "message": f"✅ Giriş başarılı. Hoş geldiniz, {db_user.full_name}!",
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": db_user.id,
            "email": db_user.email,
            "full_name": db_user.full_name,
            "level_id": db_user.level_id
        }
    }
    
    
@router.get("/me", response_model=UserResponse)
def get_my_profile(current_user: User = Depends(get_current_user)):
    return current_user