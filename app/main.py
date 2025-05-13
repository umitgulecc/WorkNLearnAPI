# FastAPI uygulamasını başlatan dosya

from fastapi import FastAPI
from app.database import Base, engine
from app.routers import user
from app.routers import quiz  # 👈 bu satır gerekli
from app.routers import user_result

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
app.include_router(user_result.router)