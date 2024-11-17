from contextlib import nullcontext

import pytest

from src.api.dependencies import get_user_service
from src.api.enums import ResponseErrorCode
from src.api.exceptions import HTTPException
from src.models.schemas.users import UserCreate, UserUpdate
from tests.conftest import Storage


@pytest.fixture(scope="session")
def user_service():
    return get_user_service()


class TestUserService:
    @pytest.mark.order(1)
    @pytest.mark.parametrize(
        "name, email, password, expectation",
        [
            ("User 1", "email@domain.com", "password1", nullcontext()),
            ("User 2", "differennt_email@domain.com", "password1", nullcontext()),
            ("Duplicate User 1", "email@domain.com", "password1", pytest.raises(HTTPException)),
        ]
    )
    @pytest.mark.asyncio(loop_scope="session")
    async def test_add_user(self, user_service, name, email, password, expectation):
        user_create_payload = UserCreate(
            name=name,
            email=email,
            password=password,
        )

        with expectation as exp:
            user = await user_service.add_user(user_create_payload)
            assert user.name == user_create_payload.name
            assert user.email == user_create_payload.email

            Storage.user = user

        if exp:
            assert exp.value.detail["code"] == ResponseErrorCode.USER_ALREADY_EXISTS

    @pytest.mark.asyncio(loop_scope="session")
    async def test_update_user(self, user_service):
        user = Storage.user
        new_user_name = "Danil"
        user_update = UserUpdate(
            name=new_user_name,
        )
        updated_user = await user_service.update_user(user.id, user_update)
        assert user.id == updated_user.id
        assert updated_user.name == new_user_name

    @pytest.mark.asyncio(loop_scope="session")
    async def test_get_user(self, user_service):
        user = Storage.user

        db_user = await user_service.get_user(user_id=user.id)
        assert user.id == db_user.id
