# Veritabanı bağlantısı
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Veritabanı bağlantı URL'si (kendi kullanıcı adı, şifre, veritabanı adıyla değiştir)
DATABASE_URL="postgresql://postgres:260122Eu@localhost:5432/WorkNLearn"
# SQLAlchemy veritabanı motorunu oluşturur
engine = create_engine(DATABASE_URL)

# Veritabanı oturumlarını yöneten yapı (veri işlemlerinde kullanacağız)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# SQLAlchemy'nin ORM tabloları için temel sınıf
Base = declarative_base()


# ✅ Eksik olan kısım bu:
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()