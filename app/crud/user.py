 # User Tablosu Veritabanı işlemleri
 
from sqlalchemy.orm import Session
from app.models.user import User
from app.utils import hash_password

# Kullanıcıyı oluştur
def create_user(db: Session, email: str, full_name: str, password: str):
    hashed_pw = hash_password(password)
    user = User(email=email, full_name=full_name, password_hash=hashed_pw, level_id= 1)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

# Email ile kullanıcıyı bul
def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def get_user_by_id(db: Session, user_id: int):
    """
    Verilen user_id ile kullanıcıyı getirir.
    Kullanıcı profili veya ilerleme ekranları için kullanılır.
    """
    return db.query(User).filter(User.id == user_id).first()


def update_user_level(db: Session, user_id: int, new_level_id: int):
    """
    Kullanıcının seviyesini (level_id) verilen değere günceller.
    Seviye atlama durumlarında kullanılır.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        user.level_id = new_level_id
        db.commit()
    return user
