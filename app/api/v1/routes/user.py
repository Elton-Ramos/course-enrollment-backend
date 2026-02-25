from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID

from app.dependency.deps import get_db, get_current_user, admin_only
from app.schemas.user import UserRead, Response, UserActivate
from app.services.user import UserService

router = APIRouter()


# ===========================
# CURRENT USER
# ===========================

@router.get("/me", response_model=UserRead, status_code=200)
def get_current_user_profile(
    current_user=Depends(get_current_user),
):
    return current_user


# ===========================
# GET USER BY EMAIL
# ===========================

@router.get("/{email}", response_model=UserRead, status_code=200)
def get_user_by_email(
    email: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    if current_user.role != "admin" and current_user.email != email:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this resource",
        )

    user = UserService.get_user_by_email(db, email)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return user


# ===========================
# LIST ALL USERS (ADMIN)
# ===========================

@router.get("", response_model=Response, status_code=200)
def get_all_users(
    db: Session = Depends(get_db),
    admin=Depends(admin_only),
):
    users = UserService.get_all_users(db)

    return Response(
        status="success",
        message="Users retrieved successfully",
        data=users or [],
    )


# ===========================
# ACTIVATE / DEACTIVATE USER
# ===========================

@router.patch(
    "/{user_id}/activate",
    response_model=UserRead,
    status_code=status.HTTP_200_OK,
)
def activate_or_deactivate_user(
    user_id: UUID,
    payload: UserActivate,
    db: Session = Depends(get_db),
    admin=Depends(admin_only),
):
    """
    Admin-only endpoint to activate or deactivate a user account.
    """

    result = UserService.update_user_status(
        db=db,
        user_id=user_id,
        is_active=payload.is_active,
    )

    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    if result == "no_state_change":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already in requested state",
        )

    return result