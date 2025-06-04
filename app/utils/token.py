from datetime import datetime, timedelta
from jose import jwt, JWTError

SECRET_KEY = "AAAAAA_BBBBB_CCC"
ALGORITHM = "HS256"

def create_reset_token(email: str, expires_minutes: int = 30):
    expire = datetime.utcnow() + timedelta(minutes=expires_minutes)
    payload = {"sub": email, "exp": expire}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def verify_reset_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except JWTError:
        return None
