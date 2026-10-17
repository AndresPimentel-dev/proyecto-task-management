from datetime import UTC, datetime, timedelta

import bcrypt
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app.models import UsersTable

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.algorithm
TIME_TO_EXPIRE = settings.access_token_expire_minutes

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1.0/auth/login")


def get_password_hash(plain_password: str):
    by_password = plain_password[:72].encode("utf-8")
    hashed = bcrypt.hashpw(by_password, bcrypt.gensalt())
    return hashed.decode("utf-8")


def verify_password(plain_password: str, hashed_password: str):
    return bcrypt.checkpw(
        plain_password[:72].encode("utf-8"), hashed_password.encode("utf-8")
    )


def create_access_token(data: dict):
    to = data.copy()
    expire = datetime.now(UTC) + timedelta(minutes=TIME_TO_EXPIRE)
    to.update({"exp": expire})
    return jwt.encode(to, SECRET_KEY, ALGORITHM)


def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            return None
    except jwt.PyJWTError:
        return None
    return email


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    email = decode_token(token)
    if email is None:
        raise credentials_exception
    user = db.query(UsersTable).filter(UsersTable.email == email).first()
    if user is None:
        raise credentials_exception
    return user