from typing import List
from uuid import UUID

from sqlalchemy.orm import Session

from app.db.models.course import Course
from app.db.models.enrollment import Enrollment
from app.schemas.course import CourseBase, CourseUpdate


class CourseService:
    """
    CourseService contains all business rules related to course lifecycle.
    It intentionally exposes only behaviors that are reachable via API routes.
    """

    @staticmethod
    def create_course(db: Session, course_data: CourseBase):
        # Business rule: capacity must be positive
        if course_data.capacity <= 0:
            return "invalid_capacity"

        # Business rule: course_code must be unique
        if (
            db.query(Course)
            .filter(Course.course_code == course_data.course_code)
            .first()
        ):
            return "course_code_exists"

        course = Course(
            title=course_data.title,
            course_code=course_data.course_code,
            capacity=course_data.capacity,
            is_active=course_data.is_active,
        )

        db.add(course)
        db.commit()
        db.refresh(course)

        return course

    @staticmethod
    def get_active_courses(db: Session) -> List[Course]:
        return (
            db.query(Course)
            .filter(Course.is_active.is_(True))
            .all()
        )

    @staticmethod
    def get_course_by_id(db: Session, course_id: UUID):
        return (
            db.query(Course)
            .filter(Course.id == course_id)
            .first()
        )

    @staticmethod
    def update_course(
        db: Session,
        course_id: UUID,
        course_data: CourseUpdate,
    ):
        course = (
            db.query(Course)
            .filter(Course.id == course_id)
            .first()
        )

        if not course:
            return None

        # Business rule: capacity cannot be zero or negative
        if (
            course_data.capacity is not None
            and course_data.capacity <= 0
        ):
            return "invalid_capacity"

        # Business rule: prevent duplicate course_code on update
        if (
            course_data.course_code
            and course_data.course_code != course.course_code
        ):
            if (
                db.query(Course)
                .filter(Course.course_code == course_data.course_code)
                .first()
            ):
                return "course_code_exists"

        for field, value in course_data.model_dump(
            exclude_unset=True
        ).items():
            setattr(course, field, value)

        db.commit()
        db.refresh(course)

        return course

    @staticmethod
    def remove_course(db: Session, course_id: UUID):
        course = (
            db.query(Course)
            .filter(Course.id == course_id)
            .first()
        )

        if not course:
            return None

        # Business rule: course with enrollments cannot be deleted
        if (
            db.query(Enrollment)
            .filter(Enrollment.course_id == course_id)
            .first()
        ):
            return "course_has_enrollments"

        db.delete(course)
        db.commit()

        return True