from datetime import datetime
from app.test.helpers import admin_login, register_user, login_user


def create_course(client, token, title, code, capacity, active=True):
    response = client.post(
        "/api/v1/course",
        json={
            "title": title,
            "course_code": code,
            "capacity": capacity,
            "is_active": active,
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 201
    return response.json()["id"]


def test_enroll_success(client):
    admin_token = admin_login(client)

    course_id = create_course(
        client, admin_token, "Creole", "CR-1", 2
    )

    student = register_user(
        client, "João", "joao@cv.com", "student", True, "pass"
    )
    token = login_user(client, "joao@cv.com", "pass")

    res = client.post(
        "/api/v1/enrollment",
        json={
            "user_id": student["id"],
            "course_id": course_id,
            "created_at": datetime.utcnow().isoformat(),
        },
        headers={"Authorization": f"Bearer {token}"},
    )

    assert res.status_code == 201


def test_enroll_inactive_course(client):
    admin_token = admin_login(client)

    course_id = create_course(
        client, admin_token, "History", "CR-2", 2, False
    )

    student = register_user(
        client, "Maria", "maria@cv.com", "student", True, "pass"
    )
    token = login_user(client, "maria@cv.com", "pass")

    res = client.post(
        "/api/v1/enrollment",
        json={
            "user_id": student["id"],
            "course_id": course_id,
            "created_at": datetime.utcnow().isoformat(),
        },
        headers={"Authorization": f"Bearer {token}"},
    )

    assert res.status_code == 409
    assert "not active" in res.json()["detail"].lower()


def test_enroll_course_full(client):
    admin_token = admin_login(client)

    course_id = create_course(
        client, admin_token, "Variants", "CR-3", 1
    )

    student1 = register_user(
        client, "Pedro", "pedro@cv.com", "student", True, "pass"
    )
    token1 = login_user(client, "pedro@cv.com", "pass")

    client.post(
        "/api/v1/enrollment",
        json={
            "user_id": student1["id"],
            "course_id": course_id,
            "created_at": datetime.utcnow().isoformat(),
        },
        headers={"Authorization": f"Bearer {token1}"},
    )

    student2 = register_user(
        client, "Ana", "ana@cv.com", "student", True, "pass"
    )
    token2 = login_user(client, "ana@cv.com", "pass")

    res = client.post(
        "/api/v1/enrollment",
        json={
            "user_id": student2["id"],
            "course_id": course_id,
            "created_at": datetime.utcnow().isoformat(),
        },
        headers={"Authorization": f"Bearer {token2}"},
    )

    assert res.status_code == 409
    assert "capacity" in res.json()["detail"].lower()


def test_enroll_already_enrolled(client):
    admin_token = admin_login(client)

    course_id = create_course(
        client, admin_token, "Evolution", "CR-4", 2
    )

    student = register_user(
        client, "Manuel", "manuel@cv.com", "student", True, "pass"
    )
    token = login_user(client, "manuel@cv.com", "pass")

    payload = {
        "user_id": student["id"],
        "course_id": course_id,
        "created_at": datetime.utcnow().isoformat(),
    }

    client.post(
        "/api/v1/enrollment",
        json=payload,
        headers={"Authorization": f"Bearer {token}"},
    )

    res = client.post(
        "/api/v1/enrollment",
        json=payload,
        headers={"Authorization": f"Bearer {token}"},
    )

    assert res.status_code == 409