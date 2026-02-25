from app.test.helpers import register_user, login_user


# ===========================
# CURRENT USER
# ===========================

def test_get_current_user(client):
    register_user(
        client,
        full_name="Normal User",
        email="user1@cv.com",
        role="student",
        is_active=True,
        password="password",
    )

    token = login_user(client, "user1@cv.com", "password")

    response = client.get(
        "/api/v1/user/me",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert response.json()["email"] == "user1@cv.com"


def test_get_current_user_unauthorized(client):
    response = client.get("/api/v1/user/me")
    assert response.status_code == 401


# ===========================
# GET USER BY EMAIL
# ===========================

def test_admin_can_get_user_by_email(client):
    register_user(
        client,
        full_name="System Admin",
        email="admin@cv.com",
        role="admin",
        is_active=True,
        password="adminpass",
    )

    admin_token = login_user(client, "admin@cv.com", "adminpass")

    register_user(
        client,
        full_name="Student User",
        email="student@cv.com",
        role="student",
        is_active=True,
        password="studentpass",
    )

    response = client.get(
        "/api/v1/user/student@cv.com",
        headers={"Authorization": f"Bearer {admin_token}"},
    )

    assert response.status_code == 200
    assert response.json()["email"] == "student@cv.com"


def test_admin_get_user_not_found(client):
    register_user(
        client,
        full_name="Admin",
        email="admin@cv.com",
        role="admin",
        is_active=True,
        password="adminpass",
    )

    admin_token = login_user(client, "admin@cv.com", "adminpass")

    response = client.get(
        "/api/v1/user/unknown@cv.com",
        headers={"Authorization": f"Bearer {admin_token}"},
    )

    assert response.status_code == 404


def test_student_cannot_access_other_user(client):
    register_user(
        client,
        full_name="Student One",
        email="student1@cv.com",
        role="student",
        is_active=True,
        password="pass1",
    )

    register_user(
        client,
        full_name="Student Two",
        email="student2@cv.com",
        role="student",
        is_active=True,
        password="pass2",
    )

    token = login_user(client, "student1@cv.com", "pass1")

    response = client.get(
        "/api/v1/user/student2@cv.com",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 403


# ===========================
# LOGIN RULES
# ===========================

def test_inactive_user_cannot_login(client):
    register_user(
        client,
        full_name="Inactive User",
        email="inactive@cv.com",
        role="student",
        is_active=False,
        password="inactivepass",
    )

    response = client.post(
        "/api/v1/auth/login",
        data={"username": "inactive@cv.com", "password": "inactivepass"},
    )

    assert response.status_code == 403


# ===========================
# LIST USERS
# ===========================

def test_admin_can_list_all_users(client):
    register_user(
        client,
        full_name="Admin User",
        email="admin@cv.com",
        role="admin",
        is_active=True,
        password="adminpass",
    )

    admin_token = login_user(client, "admin@cv.com", "adminpass")

    register_user(client, "User1", "u1@cv.com", "student", True, "pass")
    register_user(client, "User2", "u2@cv.com", "student", True, "pass")

    response = client.get(
        "/api/v1/user",
        headers={"Authorization": f"Bearer {admin_token}"},
    )

    assert response.status_code == 200
    assert response.json()["status"] == "success"
    assert isinstance(response.json()["data"], list)


def test_non_admin_cannot_list_users(client):
    register_user(
        client,
        full_name="Student",
        email="student@cv.com",
        role="student",
        is_active=True,
        password="studentpass",
    )

    token = login_user(client, "student@cv.com", "studentpass")

    response = client.get(
        "/api/v1/user",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 403


# ===========================
# ACTIVATE / DEACTIVATE USER
# ===========================

def test_admin_can_activate_user(client):
    register_user(
        client,
        full_name="Admin",
        email="admin@cv.com",
        role="admin",
        is_active=True,
        password="adminpass",
    )
    admin_token = login_user(client, "admin@cv.com", "adminpass")

    student = register_user(
        client,
        full_name="Inactive Student",
        email="inactive_student@cv.com",
        role="student",
        is_active=False,
        password="password",
    )

    response = client.patch(
        f"/api/v1/user/{student['id']}/activate",
        json={"is_active": True},
        headers={"Authorization": f"Bearer {admin_token}"},
    )

    assert response.status_code == 200
    assert response.json()["is_active"] is True


def test_non_admin_cannot_activate_user(client):
    student = register_user(
        client,
        full_name="Student",
        email="student@cv.com",
        role="student",
        is_active=True,
        password="password",
    )
    token = login_user(client, "student@cv.com", "password")

    response = client.patch(
        f"/api/v1/user/{student['id']}/activate",
        json={"is_active": False},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 403