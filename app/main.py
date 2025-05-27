# FastAPI uygulamasını başlatan dosya

from fastapi import FastAPI
from app.database import Base, engine
from app.routers import user, quiz, submission, review, personalized_quiz, team, stats


app = FastAPI( 
    title="WORK-N-LEARN API",
    description="İş İngilizcesi öğrenme sistemine ait tüm endpoint dokümantasyonu",
    version="1.0.0"
    )

Base.metadata.create_all(bind=engine)

# Ana endpoint
@app.get("/")
def root():
    return {"message": "WORK-N-LEARN API çalışıyor!"}

app.include_router(user.router)
app.include_router(quiz.router)
app.include_router(submission.router)
app.include_router(review.router)
app.include_router(personalized_quiz.router)
app.include_router(team.router)
app.include_router(stats.router)