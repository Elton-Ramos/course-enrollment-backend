from fastapi import APIRouter, status, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.dependency.deps import get_db
from app.schemas.user import UserCreate, UserRead
from app.schemas.auth import Token
from app.services.user import UserService
from app.core.security import verify_password, create_access_token

router = APIRouter()


@router.post(
    "/register",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
)
def register(
    user_data: UserCreate,
    db: Session = Depends(get_db),
):
    result = UserService.create_user(db, user_data)

    if result == "user_exists":
        raise HTTPException(
            status_code=409,
            detail="User already exists",
        )

    return result


@router.post(
    "/login",
    response_model=Token,
    status_code=status.HTTP_200_OK,
)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = UserService.get_user_by_email(db, form_data.username)

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password",
        )

    if not verify_password(
        form_data.password,
        user.hashed_password,
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password",
        )

    if not user.is_active:
        raise HTTPException(
            status_code=403,
            detail="Inactive user",
        )

    token = create_access_token(email=user.email)

    return {
        "access_token": token,
        "token_type": "bearer",
    }