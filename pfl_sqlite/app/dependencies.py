# app/dependencies.py

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from app.database import SessionLocal
from app.models.user import User
from app.core.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials"
    )

    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        user_id: int = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise credentials_exception

    return user


# 🔒 Admin-only Access
def require_admin(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admins only")
    return current_user


# 🔒 Manager-only Access (optional use)
def require_manager(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role != "manager":
        raise HTTPException(status_code=403, detail="Managers only")
    return current_user


# 🔒 Same-Club Access for Finances / Training
def require_same_club_or_admin(
    club_id: int,
    current_user: User = Depends(get_current_user)
) -> User:
    if current_user.role == "admin":
        return current_user
    if current_user.role == "manager" and current_user.club_id == club_id:
        return current_user
    raise HTTPException(status_code=403, detail="Access denied: not your club")

def restrict_to_club(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not current_user.club_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access restricted to club managers only",
        )
    return current_user