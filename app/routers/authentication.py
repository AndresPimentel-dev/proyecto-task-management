from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.auth import create_access_token, get_password_hash, verify_password
from app.database import get_db
from app.models import UsersTable
from app.schemas import TokenResponse, UserCreate

router = APIRouter(prefix="/api/v1.0", tags=["Authentication"])

# ==========================================
#          ENDPOINTS DE AUTENTICACIÓN
# ==========================================


@router.post(
    "/auth/register",
    status_code=status.HTTP_201_CREATED,
    response_model=TokenResponse,
)
def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    existing_user = (
        db.query(UsersTable)
        .filter(
            or_(
                UsersTable.email == user_data.email,
                UsersTable.username == user_data.username,
            )
        )
        .first()
    )
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email or username already registered",
        )

    hashed_pwd = get_password_hash(plain_password=user_data.password)
    new_user = UsersTable(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hashed_pwd,
    )
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except Exception:
        db.rollback()
        raise

    access_token = create_access_token(data={"sub": new_user.email})

    return {"access_token": access_token, "token_type": "bearer"}


@router.post(
    "/auth/login",
    status_code=status.HTTP_200_OK,
    response_model=TokenResponse,
)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = (
        db.query(UsersTable)
        .filter(
            or_(
                UsersTable.username == form_data.username,
                UsersTable.email == form_data.username,
            )
        )
        .first()
    )
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username/email or password",
        )

    access_token = create_access_token(data={"sub": user.email})

    return {"access_token": access_token, "token_type": "bearer"}
