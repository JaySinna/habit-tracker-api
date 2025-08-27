from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from sqlmodel import Session, select

from ..core.db import get_session
from ..core.security import hash_password, verify_password, create_access_token
from ..core.config import settings
from ..models import User
from ..schemas import UserCreate, TokenOut

router = APIRouter(prefix="/auth", tags=["auth"])

oauth2 = HTTPBearer()


@router.post("/register", status_code=201)
def register(payload: UserCreate, session: Session = Depends(get_session)):
    exists = session.exec(select(User).where(User.email == payload.email)).first()
    if exists:
        raise HTTPException(status_code=400, detail="Email already registered")

    user = User(email=payload.email, password_hash=hash_password(payload.password))
    session.add(user)
    session.commit()
    session.refresh(user)
    return {"id": user.id, "email": user.email}


@router.post("/login", response_model=TokenOut)
def login(payload: UserCreate, session: Session = Depends(get_session)):
    user = session.exec(select(User).where(User.email == payload.email)).first()
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(sub=str(user.id))
    return TokenOut(access_token=token)


def get_current_user(
    token: HTTPAuthorizationCredentials = Depends(oauth2),
    session: Session = Depends(get_session),
) -> User:
    try:
        data = jwt.decode(
            token.credentials,
            settings.JWT_SECRET,
            algorithms=[settings.JWT_ALGO]
        )
        user_id = int(data.get("sub"))
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user
