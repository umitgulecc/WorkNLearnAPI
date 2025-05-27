from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.auth.auth import get_current_user
from app.models.department import Department
from app.models.skill import Skill
from app.models.user import User
from app.database import SessionLocal
from app.models.user_skill_score import UserSkillScore
from app.schemas.user import SkillScoreOut, UserCreate, UserProfile,UserLogin
from app.crud.user import create_user, get_user_by_email
from app.utils.password import verify_password
from app.auth.auth import create_access_token
from app.schemas.user import UserUpdate
from app.schemas.user import UserBasicOut
from app.crud.user import get_all_users
from app.utils.permissions import has_access_to_user, is_manager
from app.schemas.user import ForgotPasswordRequest, ResetPasswordRequest
from app.utils.token import create_reset_token, verify_reset_token

router = APIRouter(prefix="", tags=["🧍 Kullanıcı İşlemleri"])  # <-- BU SATIR ÇOK ÖNEMLİ

# Veritabanı bağlantısı
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register")
def register(
    user: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # ⛔ Sadece role_id 1 (admin) veya 2 (müdür) izinli
    if current_user.role_id not in [1, 2]:
        raise HTTPException(status_code=403, detail="Bu işlemi yapma yetkiniz yok.")

    # Zaten kayıtlı mı?
    if get_user_by_email(db, user.email):
        raise HTTPException(status_code=400, detail="❌ Bu e-posta adresi zaten kayıtlı.")
    
    # Yeni kullanıcı oluştur
    created_user = create_user(db, user.email, user.full_name, user.password, user.role_id, user.department_id)
    
    return {
        "message": f"✅ Kayıt başarılı. Hoş geldiniz, {created_user.full_name}!",
        "user": {
            "id": created_user.id,
            "email": created_user.email,
            "full_name": created_user.full_name,
            "role_id": created_user.role_id,
            "department_id": created_user.department_id,
        }
    }


@router.post("/login")
def login(request: UserLogin, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, request.email)

    if not db_user or not verify_password(request.password, db_user.password_hash):
        raise HTTPException(status_code=401, detail="E-posta veya şifre hatalı.")

    if db_user.department_id != request.department_id:
        raise HTTPException(status_code=403, detail="Departman bilgisi uyuşmuyor.")

    token = create_access_token(data={"sub": db_user.email})

    return {
        "message": f"✅ Giriş başarılı. Hoş geldiniz, {db_user.full_name}!",
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": db_user.id,
            "email": db_user.email,
            "full_name": db_user.full_name,
            "level_id": db_user.level_id,
            "role_id": db_user.role_id,
            "department_id": db_user.department_id
        }
    }

    
    
# @router.get("/me", response_model=UserResponse)
# def get_my_profile(current_user: User = Depends(get_current_user)):
#     return current_user


@router.get("/me", response_model=UserProfile)
def get_my_profile(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Kullanıcı skorlarını al
    scores = (
        db.query(UserSkillScore, Skill)
        .join(Skill, UserSkillScore.skill_id == Skill.id)
        .filter(UserSkillScore.user_id == current_user.id)
        .all()
    )

    skill_scores = [
        SkillScoreOut(
            skill_id=score.skill_id,
            skill_name=skill.name,
            total_score=score.total_score
        )
        for score, skill in scores
    ]

    return UserProfile(
        id=current_user.id,
        full_name=current_user.full_name,
        email=current_user.email,
        level_id=current_user.level_id,
        skill_scores=skill_scores
    )
    
    
@router.put("/me", response_model=UserBasicOut)
def update_my_profile(
    updates: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Kullanıcının kendi adını ve şifresini güncellemesine izin verir.
    """
    # Oturuma bağlı hale getir
    user = db.merge(current_user)

    if updates.full_name:
        user.full_name = updates.full_name
    if updates.password:
        from app.utils import hash_password
        user.password_hash = hash_password(updates.password)

    db.commit()
    db.refresh(user)
    return user


@router.delete("/me", status_code=200)
def delete_my_account(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Kullanıcının kendi hesabını silmesini sağlar.
    """
    user = db.merge(current_user)
    db.delete(user)
    db.commit()
    return {"detail": "✅ Hesabınız başarıyla silindi."}



@router.get("/all-users", response_model=list[UserBasicOut])
def list_all_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # ✅ Erişim kontrolü: yalnızca Genel Müdür görebilir
    if not is_manager(current_user):
        raise HTTPException(status_code=403, detail="Bu veriye yalnızca genel müdür erişebilir.")

    return get_all_users(db)



@router.get("/user/{user_id}", response_model=UserProfile)
def get_user_profile(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    target_user = db.query(User).filter_by(id=user_id).first()
    if not target_user:
        raise HTTPException(status_code=404, detail="Kullanıcı bulunamadı.")

    # Yetki kontrolü
    if not has_access_to_user(current_user, target_user):
        raise HTTPException(status_code=403, detail="Bu kullanıcıya erişim yetkiniz yok.")

    # Skill skorlarıyla birlikte profili oluştur
    scores = (
        db.query(UserSkillScore, Skill)
        .join(Skill, UserSkillScore.skill_id == Skill.id)
        .filter(UserSkillScore.user_id == target_user.id)
        .all()
    )

    skill_scores = [
        SkillScoreOut(
            skill_id=score.skill_id,
            skill_name=skill.name,
            total_score=score.total_score
        )
        for score, skill in scores
    ]

    return UserProfile(
        id=target_user.id,
        full_name=target_user.full_name,
        email=target_user.email,
        level_id=target_user.level_id,
        skill_scores=skill_scores
    )





@router.post("/forgot-password")
def forgot_password(request: ForgotPasswordRequest, db: Session = Depends(get_db)):
    user = get_user_by_email(db, request.email)
    if not user:
        raise HTTPException(status_code=404, detail="Kullanıcı bulunamadı.")
    
    reset_token = create_reset_token(user.email)

    # Gerçek projede bu link mail ile gönderilmeli
    reset_url = f"http://localhost:8000/reset-password?token={reset_token}"
    print("🔗 Şifre sıfırlama bağlantısı:", reset_url)

    return {"detail": "Şifre sıfırlama bağlantısı e-posta adresinize gönderildi (test için loglandı)."}



@router.post("/reset-password")
def reset_password(request: ResetPasswordRequest, db: Session = Depends(get_db)):
    email = verify_reset_token(request.token)
    if not email:
        raise HTTPException(status_code=400, detail="Geçersiz veya süresi dolmuş token.")

    user = get_user_by_email(db, email)
    if not user:
        raise HTTPException(status_code=404, detail="Kullanıcı bulunamadı.")

    from app.utils.password import hash_password
    user.password_hash = hash_password(request.new_password)
    db.commit()

    return {"detail": "✅ Şifreniz başarıyla güncellendi."}


@router.get("/departments")
def get_departments(db: Session = Depends(get_db)):
    departments = db.query(Department).all()
    return [{"id": d.id, "name": d.name} for d in departments]
