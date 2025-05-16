#Şifreleri Hash ile şifreleyip saklayabilmek için

from passlib.context import CryptContext

# Şifreleme algoritması olarak bcrypt kullanıyoruz
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Şifreyi hash'leme (şifreleme)
def hash_password(password: str):
    return pwd_context.hash(password)

# Şifreyi kontrol etme (giriş yaparken)
def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)
