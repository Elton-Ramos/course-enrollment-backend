from app.test.helpers import register_user, login_user


def test_user_can_register_successfully(client):
    response = client.post(
        "/api/v1/auth/register",
        json={
            "full_name": "Ana Monteiro",
            "email": "ana@cv.com",
            "role": "student",
            "is_active": True,
            "password": "securepass",
        },
    )

    assert response.status_code == 201
    assert response.json()["email"] == "ana@cv.com"


def test_registration_fails_with_duplicate_email(client):
    register_user(
        client,
        full_name="Manuel Teixeira",
        email="manuel@cv.com",
        role="student",
        is_active=True,
        password="password123",
    )

    response = client.post(
        "/api/v1/auth/register",
        json={
            "full_name": "Carlos Lima",
            "email": "manuel@cv.com",
            "role": "student",
            "is_active": True,
            "password": "password123",
        },
    )

    assert response.status_code == 409


def test_login_with_valid_credentials(client):
    register_user(
        client,
        full_name="Maria Lopes",
        email="maria@cv.com",
        role="student",
        is_active=True,
        password="mypassword",
    )

    response = client.post(
        "/api/v1/auth/login",
        data={
            "username": "maria@cv.com",
            "password": "mypassword",
        },
    )

    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"


def test_login_fails_with_wrong_password(client):
    register_user(
        client,
        full_name="João Silva",
        email="joao@cv.com",
        role="student",
        is_active=True,
        password="correctpass",
    )

    response = client.post(
        "/api/v1/auth/login",
        data={
            "username": "joao@cv.com",
            "password": "wrongpass",
        },
    )

    assert response.status_code == 401


def test_login_fails_for_inactive_user(client):
    register_user(
        client,
        full_name="Helena Rocha",
        email="helena@cv.com",
        role="student",
        is_active=False,
        password="inactivepass",
    )

    response = client.post(
        "/api/v1/auth/login",
        data={
            "username": "helena@cv.com",
            "password": "inactivepass",
        },
    )

    assert response.status_code == 403