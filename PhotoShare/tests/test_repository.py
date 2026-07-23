import pytest
from PhotoShare.repository.users import create_user, get_user_by_email
from PhotoShare.database.models import Role

@pytest.mark.asyncio
async def test_first_user_becomes_admin(db_session):
    user = await create_user(db_session, "firstuser", "first@test.com", "hashed_pw")
    assert user.role == Role.ADMIN


@pytest.mark.asyncio
async def test_get_user_by_email_returns_none_for_unknown_email(db_session):
    result = await get_user_by_email(db_session, "doesnotexist@test.com")
    assert result is None