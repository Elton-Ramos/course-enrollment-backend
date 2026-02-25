from uuid import UUID

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.schemas.course import (
    CourseRead,
    CourseCreate,
    CourseUpdate,
    Response,
)
from app.dependency.deps import get_current_user, get_db, admin_only
from app.services.course import CourseService

router = APIRouter()


@router.post("", response_model=CourseRead, status_code=201)
def create_course(
    course_data: CourseCreate,
    db: Session = Depends(get_db),
    admin=Depends(admin_only),
):
    course = CourseService.create_course(db, course_data)

    if course == "invalid_capacity":
        raise HTTPException(
            status_code=409,
            detail="Course capacity must be greater than zero",
        )

    if course == "course_code_exists":
        raise HTTPException(
            status_code=409,
            detail="Course code already exists",
        )

    if course == "course_title_exists":
        raise HTTPException(
            status_code=409,
            detail="Course title already exists",
        )

    return course


@router.get("", response_model=Response, status_code=200)
def get_active_courses(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    courses = CourseService.get_active_courses(db)
    return Response(
        status="success",
        message="Active courses retrieved",
        data=courses,
    )


@router.get("/all", response_model=Response, status_code=200)
def get_all_courses(
    db: Session = Depends(get_db),
    admin=Depends(admin_only),
):
    courses = CourseService.get_all_courses(db)
    return Response(
        status="success",
        message="All courses retrieved",
        data=courses,
    )


@router.get("/inactive", response_model=Response, status_code=200)
def get_inactive_courses(
    db: Session = Depends(get_db),
    admin=Depends(admin_only),
):
    courses = CourseService.get_inactive_courses(db)
    return Response(
        status="success",
        message="Inactive courses retrieved",
        data=courses,
    )


@router.get("/{course_id}", response_model=Response, status_code=200)
def get_course_by_id(
    course_id: UUID,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    course = CourseService.get_course_by_id(db, course_id)

    if not course:
        raise HTTPException(
            status_code=404,
            detail="Course not found",
        )

    return Response(
        status="success",
        message="Course retrieved",
        data=course,
    )


@router.patch("/{course_id}", response_model=CourseRead, status_code=200)
def update_course(
    course_id: UUID,
    course_data: CourseUpdate,
    db: Session = Depends(get_db),
    admin=Depends(admin_only),
):
    course = CourseService.update_course(
        db,
        course_id,
        course_data,
    )

    if course is None:
        raise HTTPException(
            status_code=404,
            detail="Course not found",
        )

    if course == "invalid_capacity":
        raise HTTPException(
            status_code=409,
            detail="Course capacity must be greater than zero",
        )

    if course == "course_code_exists":
        raise HTTPException(
            status_code=409,
            detail="Course code already exists",
        )

    return course


@router.delete("/{course_id}", status_code=200)
def delete_course(
    course_id: UUID,
    db: Session = Depends(get_db),
    admin=Depends(admin_only),
):
    result = CourseService.remove_course(db, course_id)

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Course not found",
        )

    if result == "course_has_enrollments":
        raise HTTPException(
            status_code=409,
            detail="Cannot delete course with active enrollments",
        )

    return {"message": "Course removed successfully"}