import pytest

from tests.rest.models.model import UserRequestDto


def test_delete_user(create_user, user_repository, users_api):
    assert users_api.delete(create_user.id).status_code == 200
    assert user_repository.get_by_id(create_user.id) is None


def test_get_user_id(users_api, temp_user):
    user = users_api.get_by_id(temp_user.id)
    assert user.id == temp_user.id
    assert user.username == temp_user.details.username
    assert user.email == temp_user.details.email
    assert user.role == temp_user.details.role


@pytest.mark.parametrize(
    ("username", "email", "password", "role"),
    [
        ("username-test", "email-test@email.com", "password", "CUSTOMER"),
        ("new-user", "new-user@email.com", "123456", "ADMIN"),
    ],
)
def test_update_user(temp_user, users_api, user_repository, username, email, password, role):
    users_api.update(
        temp_user.id,
        UserRequestDto(username=username, email=email, password=password, role=role),
    )
    updated_user = user_repository.get_by_id(temp_user.id)
    assert updated_user.get("username") == username
    assert updated_user.get("email") == email
    assert updated_user.get("role") == role


def test_create_user(users_api, user_repository, delete_users, faker_instance):
    dto = UserRequestDto(
        username=faker_instance.first_name(),
        email=faker_instance.email(),
        password=faker_instance.password(),
        role="CUSTOMER",
    )
    response = users_api.create(dto)
    created_user = user_repository.get_by_id(response.id)
    delete_users.append(response.id)
    assert created_user.get("username") == dto.username
    assert created_user.get("email") == dto.email
    assert created_user.get("role") == dto.role


