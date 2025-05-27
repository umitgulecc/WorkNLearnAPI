 # User Tablosu Veritabanı işlemleri
 
from sqlalchemy.orm import Session
from app.models.user import User
from app.utils.password import hash_password
from sqlalchemy import func
from app.models.user_quiz_result import UserQuizResult

# Kullanıcıyı oluştur
def create_user(db: Session, email: str, full_name: str, password: str, role_id: int = 3, department_id: int = None):
    hashed_pw = hash_password(password)
    user = User(email=email, full_name=full_name, password_hash=hashed_pw, level_id= 1, role_id= role_id, department_id=department_id)  
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


def update_user_password(db: Session, user_id: int, new_password: str):
    """
    Kullanıcının şifresini günceller.
    """
    from app.utils import hash_password
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        user.password_hash = hash_password(new_password)
        db.commit()
        return True
    return False


def get_all_users(db: Session):
    """
    Tüm kullanıcıları getirir.
    (Yönetici sayfası, test, analiz vs. için kullanılabilir)
    """
    return db.query(User).all()


def delete_user(db: Session, user_id: int):
    """
    Belirtilen ID'ye sahip kullanıcıyı siler.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        db.delete(user)
        db.commit()
        return True
    return False


def get_user_total_score(db: Session, user_id: int) -> float:
    total = db.query(func.sum(UserQuizResult.score))\
              .filter(UserQuizResult.user_id == user_id)\
              .scalar()
    return total or 0.0
