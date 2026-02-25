from uuid import UUID
from sqlalchemy.orm import Session
from app.db.models.user import User
from app.schemas.user import UserCreate
from app.core.security import get_password_hash


class UserService:

    @staticmethod
    def get_user_by_email(db: Session, email: str):
        return (
            db.query(User)
            .filter(User.email == email)
            .first()
        )

    @staticmethod
    def create_user(db: Session, user_data: UserCreate):
        existing_user = (
            db.query(User)
            .filter(User.email == user_data.email)
            .first()
        )

        if existing_user:
            return "user_exists"

        user = User(
            full_name=user_data.full_name,
            email=user_data.email,
            hashed_password=get_password_hash(user_data.password),
            role=user_data.role,
            is_active=user_data.is_active,
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        return user

    @staticmethod
    def get_user_by_id(db: Session, user_id: UUID):
        return (
            db.query(User)
            .filter(User.id == user_id)
            .first()
        )

    @staticmethod
    def get_all_users(db: Session):
        return db.query(User).all()

   
    @staticmethod
    def update_user_status(
        db: Session,
        user_id: UUID,
        is_active: bool,
    ):
        user = (
            db.query(User)
            .filter(User.id == user_id)
            .first()
        )

        if not user:
            return None

        if user.is_active == is_active:
            return "no_state_change"

        user.is_active = is_active
        db.commit()
        db.refresh(user)

        return user