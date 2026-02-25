from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependency.deps import get_db, get_current_user, admin_only
from app.schemas.enrollment import EnrollmentCreate, EnrollmentRead, Response
from app.services.enrollment import EnrollmentService

router = APIRouter()


@router.get("", response_model=Response, status_code=200)
def get_all_enrollments(
    db: Session = Depends(get_db),
    admin=Depends(admin_only),
):
    enrollments = EnrollmentService.get_all_enrollment(db)
    return Response(
        status="success",
        message="Enrollments retrieved successfully",
        data=enrollments or [],
    )


@router.get("/user", response_model=Response, status_code=200)
def get_user_enrollments(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    enrollments = EnrollmentService.get_enrollment_for_a_student(
        db,
        current_user.id,
    )
    return Response(
        status="success",
        message="User enrollments retrieved successfully",
        data=enrollments or [],
    )


@router.get("/{enrollment_id}", response_model=EnrollmentRead, status_code=200)
def get_enrollment_by_id(
    enrollment_id: UUID,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    enrollment = EnrollmentService.get_enrollment_by_id(
        db,
        enrollment_id,
    )

    if not enrollment:
        raise HTTPException(
            status_code=404,
            detail="Enrollment not found",
        )

    return enrollment


@router.post("", response_model=EnrollmentRead, status_code=201)
def enroll_in_course(
    enrollment_data: EnrollmentCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    if current_user.role == "admin":
        raise HTTPException(
            status_code=403,
            detail="Admins are not allowed to enroll in courses",
        )

    result = EnrollmentService.enroll_course(db, enrollment_data)

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Course not found",
        )

    if result == "course_not_active":
        raise HTTPException(
            status_code=409,
            detail="Course is not active",
        )

    if result == "course_is_full":
        raise HTTPException(
            status_code=409,
            detail="Course capacity has been reached",
        )

    if result == "already_enrolled":
        raise HTTPException(
            status_code=409,
            detail="Student is already enrolled in this course",
        )

    return result


@router.delete("/{course_id}", status_code=200)
def remove_student_from_course(
    course_id: UUID,
    user_id: UUID,
    db: Session = Depends(get_db),
    admin=Depends(admin_only),
):
    removed = EnrollmentService.remove_student_from_enrollment(
        db,
        user_id,
        course_id,
    )

    if not removed:
        raise HTTPException(
            status_code=404,
            detail="Enrollment not found",
        )

    return {"message": "Student removed from course successfully"}


@router.get("/course/{course_id}", response_model=Response, status_code=200)
def get_course_enrollments(
    course_id: UUID,
    db: Session = Depends(get_db),
    admin=Depends(admin_only),
):
    enrollments = EnrollmentService.get_enrollment_for_a_course(
        db,
        course_id,
    )
    return Response(
        status="success",
        message="Course enrollments retrieved successfully",
        data=enrollments or [],
    )