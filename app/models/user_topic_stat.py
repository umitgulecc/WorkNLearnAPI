from sqlalchemy import Column, Integer, ForeignKey
from app.database import Base
from app.models.topic import Topic
from app.models.user import User  

class UserTopicStat(Base):
    __tablename__ = "user_topic_stats"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    topic_id = Column(Integer, ForeignKey(Topic.id), nullable=False)
    wrong_count = Column(Integer, default=0)
