from app.test.helpers import admin_login, register_user, login_user

# ===========================
# COURSE ROUTE TESTS
# ===========================

# These tests validate:
# - Course creation rules
# - Data validation constraints
# - Read operations
# - Error handling for invalid requests
# - Permission enforcement


# ===========================
# CREATE COURSE
# ===========================

def test_admin_create_course(client):
    """Admin can create a new course"""
    token = admin_login(client)

    response = client.post(
        "/api/v1/course",
        json={
            "title": "Basic Cape Verdean Creole",
            "course_code": "CVK-101",
            "capacity": 20,
            "is_active": True,
        },
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 201
    assert response.json()["course_code"] == "CVK-101"


# ===========================
# VALIDATION RULES
# ===========================

def test_course_duplicate_code(client):
    """Course code must be unique"""
    token = admin_login(client)

    client.post(
        "/api/v1/course",
        json={
            "title": "History of Cape Verde",
            "course_code": "HCV-201",
            "capacity": 25,
            "is_active": True,
        },
        headers={"Authorization": f"Bearer {token}"},
    )

    response = client.post(
        "/api/v1/course",
        json={
            "title": "Advanced History of Cape Verde",
            "course_code": "HCV-201",
            "capacity": 30,
            "is_active": True,
        },
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 409


def test_course_capacity_must_be_positive(client):
    """Course capacity cannot be zero or negative"""
    token = admin_login(client)

    response = client.post(
        "/api/v1/course",
        json={
            "title": "Cape Verdean Culture",
            "course_code": "CULT-001",
            "capacity": 0,
            "is_active": True,
        },
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 409


# ===========================
# READ COURSES
# ===========================

def test_get_active_courses(client):
    """Admin can retrieve list of active courses"""
    token = admin_login(client)

    client.post(
        "/api/v1/course",
        json={
            "title": "Variants of Cape Verdean Creole",
            "course_code": "VAR-301",
            "capacity": 15,
            "is_active": True,
        },
        headers={"Authorization": f"Bearer {token}"},
    )

    response = client.get(
        "/api/v1/course",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert isinstance(response.json()["data"], list)


def test_get_course_by_id(client):
    """Retrieve a specific course by ID"""
    token = admin_login(client)

    response = client.post(
        "/api/v1/course",
        json={
            "title": "Cape Verdean Oral Traditions",
            "course_code": "ORAL-101",
            "capacity": 10,
            "is_active": True,
        },
        headers={"Authorization": f"Bearer {token}"},
    )

    course_id = response.json()["id"]

    res = client.get(
        f"/api/v1/course/{course_id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert res.status_code == 200
    assert res.json()["data"]["id"] == course_id


# ===========================
# ERROR HANDLING
# ===========================

def test_course_not_found(client):
    """Requesting a non-existent course returns 404"""
    register_user(
        client,
        "Student",
        "student@cv.com",
        "student",
        True,
        "password",
    )

    token = login_user(client, "student@cv.com", "password")

    response = client.get(
        "/api/v1/course/00000000-0000-0000-0000-000000000000",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 404


# ===========================
# PERMISSION RULES
# ===========================

def test_student_cannot_update_course(client):
    """Students must not be allowed to update courses"""
    admin_token = admin_login(client)

    response = client.post(
        "/api/v1/course",
        json={
            "title": "Protected Course",
            "course_code": "PROT-001",
            "capacity": 10,
            "is_active": True,
        },
        headers={"Authorization": f"Bearer {admin_token}"},
    )

    course_id = response.json()["id"]

    register_user(
        client,
        "Student Two",
        "student2@cv.com",
        "student",
        True,
        "password",
    )
    student_token = login_user(client, "student2@cv.com", "password")

    res = client.patch(
        f"/api/v1/course/{course_id}",
        json={
            "title": "Illegal Update",
            "capacity": 5,
        },
        headers={"Authorization": f"Bearer {student_token}"},
    )

    assert res.status_code == 403


def test_student_cannot_delete_course(client):
    """Students must not be allowed to delete courses"""
    admin_token = admin_login(client)

    response = client.post(
        "/api/v1/course",
        json={
            "title": "Delete Protected",
            "course_code": "PROT-002",
            "capacity": 10,
            "is_active": True,
        },
        headers={"Authorization": f"Bearer {admin_token}"},
    )

    course_id = response.json()["id"]

    register_user(
        client,
        "Student Three",
        "student3@cv.com",
        "student",
        True,
        "password",
    )
    student_token = login_user(client, "student3@cv.com", "password")

    res = client.delete(
        f"/api/v1/course/{course_id}",
        headers={"Authorization": f"Bearer {student_token}"},
    )

    assert res.status_code == 403