from sqlalchemy.orm import Session
from datetime import datetime
from app.models.user_skill_score import UserSkillScore



def update_user_skill_score(db: Session, user_id: int, skill_id: int, score: float):
    existing = db.query(UserSkillScore).filter_by(user_id=user_id, skill_id=skill_id).first()
    if existing:
        existing.total_score += score
        existing.updated_at = datetime.utcnow()
    else:
        new_score = UserSkillScore(
            user_id=user_id,
            skill_id=skill_id,
            total_score=score
        )
        db.add(new_score)
    db.commit()
