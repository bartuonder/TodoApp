from .utils import *
from .utils import override_get_db
from ..routers.users import get_db, get_current_user
from fastapi import status


app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


def test_return_user(test_user):
    response = client.get("/user/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["username"] == "bartuonder"
    assert response.json()["email"] == "bartuonder@gmail.com"
    assert response.json()["first_name"] == "Bartu"
    assert response.json()["last_name"] == "Onder"
    assert response.json()["role"] == "admin"
    assert response.json()["phone_number"] == "+1 555 555 555"


def test_change_password_success(test_user):
    request = client.put("/user/change_password", json={"password": "test1234", "new_password": "test12345"})
    assert request.status_code == status.HTTP_204_NO_CONTENT


def test_change_password_failure(test_user):
    request = client.put("/user/change_password", json={"password": "test4321", "new_password": "test12345"})
    assert request.status_code == status.HTTP_401_UNAUTHORIZED
    assert request.json() == {"detail": "Password mismatch."}


def test_change_phone_number_success(test_user):
    response = client.put("/user/phonenumber/1111111")
    assert response.status_code == status.HTTP_204_NO_CONTENT
