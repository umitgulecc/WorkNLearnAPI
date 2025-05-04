# Token işlemleri (JWT)
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.crud.user import get_user_by_email
from datetime import datetime, timedelta
from jose import jwt, JWTError

# Güvenlik için kullanılacak gizli anahtar
SECRET_KEY = "cok-gizli-bir-anahtar"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 1 gün

# Token oluşturur
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Token'ı çözüp içinden kullanıcıyı bulur
def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload["sub"]
    except JWTError:
        return None


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

# DB bağımlılığı
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Kullanıcıyı token'dan çöz
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    from app.auth.auth import verify_token  # döngüsel import'ı engellemek için

    email = verify_token(token)
    if email is None:
        raise HTTPException(status_code=401, detail="❌ Geçersiz veya süresi dolmuş token.")

    user = get_user_by_email(db, email)
    if user is None:
        raise HTTPException(status_code=404, detail="❌ Kullanıcı bulunamadı.")
    
    return user