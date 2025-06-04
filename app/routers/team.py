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
from app.database import get_db


router = APIRouter(prefix="/team", tags=["👥 Takım"])
    
@router.get("/results/{user_id}", response_model=list[TeamResult])
def get_results_for_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role_id != 2:
        raise HTTPException(status_code=403, detail="Sadece müdürler erişebilir.")

    department = db.query(Department).filter(Department.manager_id == current_user.id).first()
    if not department:
        raise HTTPException(status_code=404, detail="Departman bulunamadı.")

    user = db.query(User).filter(User.id == user_id).first()
    if not user or user.department_id != department.id:
        raise HTTPException(status_code=403, detail="Bu kullanıcı sizin departmanınıza ait değil.")

    results = (
        db.query(UserQuizResult)
        .join(Quiz, UserQuizResult.quiz_id == Quiz.id)
        .filter(UserQuizResult.user_id == user_id)
        .options(joinedload(UserQuizResult.quiz))
        .all()
    )

    return [
        TeamResult(
            user_id=user.id,
            full_name=user.full_name,
            quiz_title=r.quiz.title,
            score=r.score,
            taken_at=r.taken_at,
            result_id=r.id
        ) for r in results
    ]




@router.get("/summary", response_model=list[TeamMemberSummary])
def get_team_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    print(get_current_user)
    if current_user.role_id != 2:
        raise HTTPException(status_code=403, detail="Sadece departman müdürleri erişebilir.")

    department = db.query(Department).filter(Department.manager_id == current_user.id).first()
    if not department:
        return []

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

        level_str = f"Seviye {user.level_id}"

        summary_list.append(TeamMemberSummary(
            user_id=user.id,
            full_name=user.full_name,
            level=level_str,
            total_quizzes=quiz_count,
            average_score=round(avg_score, 2),
            total_score= total_score
        ))
    print(summary_list)
    return summary_list
