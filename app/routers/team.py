from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from app.database import SessionLocal
from app.models.level import Level
from app.models.user import User
from app.models.department import Department
from app.models.quiz import Quiz
from app.models.user_quiz_result import UserQuizResult
from app.auth.auth import get_current_user
from app.schemas.team import TeamMemberSummary,TeamResult

router = APIRouter(prefix="/team", tags=["👥 Takım"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
        
@router.get("/results", response_model=list[TeamResult])
def get_team_results(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Sadece müdür görebilir
    if current_user.role_id != 2:
        raise HTTPException(status_code=403, detail="Sadece departman müdürleri erişebilir.")

    # Müdürün yönettiği departmanı al
    department = db.query(Department).filter(Department.manager_id == current_user.id).first()
    if not department:
        return []

    # Departmandaki kullanıcıların quiz sonuçlarını al
    members = (
        db.query(UserQuizResult)
        .join(User, UserQuizResult.user_id == User.id)
        .join(Quiz, UserQuizResult.quiz_id == Quiz.id)
        .filter(User.department_id == department.id)
        .options(joinedload(UserQuizResult.user), joinedload(UserQuizResult.quiz))
        .all()
    )

    results = []
    for r in members:
        results.append(TeamResult(
            user_id=r.user.id,
            full_name=r.user.full_name,
            quiz_title=r.quiz.title,
            score=r.score,
            taken_at=r.taken_at
        ))

    return results




@router.get("/summary", response_model=list[TeamMemberSummary])
def get_team_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role_id != 2:
        raise HTTPException(status_code=403, detail="Sadece departman müdürleri erişebilir.")

    department = db.query(Department).filter(Department.manager_id == current_user.id).first()
    if not department:
        return []

    # ⛔ Sadece çalışanlar (role_id == 3)
    users = (
        db.query(User)
        .filter(
            User.department_id == department.id,
            User.role_id == 3
        ).all()
    )

    summary_list = []
    for user in users:
        results = db.query(UserQuizResult).filter(UserQuizResult.user_id == user.id).all()

        if results:
            total_score = sum([r.score for r in results])
            avg_score = sum([r.score for r in results]) / len(results)
            quiz_count = len(results)
        else:
            total_score = 0
            avg_score = 0.0
            quiz_count = 0

        level_str = f"Seviye {user.level_id}"  # ✅ artık level_id doğrudan seviye numarası

        summary_list.append(TeamMemberSummary(
            user_id=user.id,
            full_name=user.full_name,
            level=level_str,
            total_quizzes=quiz_count,
            average_score=round(avg_score, 2),
            total_score= total_score
        ))

    return summary_list
