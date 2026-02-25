from fastapi.testclient import TestClient


def register_user(
    client: TestClient,
    full_name: str,
    email: str,
    role: str,
    is_active: bool,
    password: str,
):
    response = client.post(
        "/api/v1/auth/register",
        json={
            "full_name": full_name,
            "email": email,
            "role": role,
            "is_active": is_active,
            "password": password,
        },
    )
    return response.json()


def login_user(client: TestClient, email: str, password: str) -> str:
    response = client.post(
        "/api/v1/auth/login",
        data={"username": email, "password": password},
    )
    return response.json()["access_token"]


def admin_login(client: TestClient) -> str:
    register_user(
        client,
        "System Admin",
        "admin@cv.com",
        "admin",
        True,
        "adminpass",
    )
    return login_user(client, "admin@cv.com", "adminpass")