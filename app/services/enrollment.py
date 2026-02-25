from uuid import UUID
from sqlalchemy.orm import Session
from app.db.models.enrollment import Enrollment
from app.db.models.course import Course


class EnrollmentService:

    @staticmethod
    def enroll_course(db: Session, data):
        course = (
            db.query(Course)
            .filter(Course.id == data.course_id)
            .first()
        )

        if not course:
            return None

        if not course.is_active:
            return "course_not_active"

        if course.capacity <= 0:
            return "course_is_full"

        existing_enrollment = (
            db.query(Enrollment)
            .filter(
                Enrollment.course_id == data.course_id,
                Enrollment.user_id == data.user_id,
            )
            .first()
        )

        if existing_enrollment:
            return "already_enrolled"

        enrolled_count = (
            db.query(Enrollment)
            .filter(Enrollment.course_id == data.course_id)
            .count()
        )

        if enrolled_count >= course.capacity:
            return "course_is_full"

        enrollment = Enrollment(
            user_id=data.user_id,
            course_id=data.course_id,
        )

        db.add(enrollment)
        db.commit()
        db.refresh(enrollment)

        return enrollment

    @staticmethod
    def get_all_enrollment(db: Session):
        return db.query(Enrollment).all()

    @staticmethod
    def get_enrollment_for_a_student(
        db: Session,
        user_id: UUID,
    ):
        return (
            db.query(Enrollment)
            .filter(Enrollment.user_id == user_id)
            .all()
        )

    @staticmethod
    def get_enrollment_for_a_course(
        db: Session,
        course_id: UUID,
    ):
        return (
            db.query(Enrollment)
            .filter(Enrollment.course_id == course_id)
            .all()
        )

    @staticmethod
    def get_enrollment_by_id(
        db: Session,
        enrollment_id: UUID,
    ):
        return (
            db.query(Enrollment)
            .filter(Enrollment.id == enrollment_id)
            .first()
        )

    @staticmethod
    def remove_student_from_enrollment(
        db: Session,
        user_id: UUID,
        course_id: UUID,
    ):
        enrollment = (
            db.query(Enrollment)
            .filter(
                Enrollment.user_id == user_id,
                Enrollment.course_id == course_id,
            )
            .first()
        )

        if not enrollment:
            return None

        db.delete(enrollment)
        db.commit()

        return enrollment