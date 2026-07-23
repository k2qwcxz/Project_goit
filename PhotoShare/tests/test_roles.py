
import pytest
from unittest.mock import MagicMock

from PhotoShare.database.models import Role
from PhotoShare.services.roles import RoleCheker


@pytest.mark.asyncio
async def test_role_checker_allows_correct_role():
    checker = RoleCheker([Role.ADMIN, Role.MODERATOR])

    fake_admin_user = MagicMock()
    fake_admin_user.role = Role.ADMIN

    result = await checker(current_user=fake_admin_user)
    assert result == fake_admin_user


@pytest.mark.asyncio
async def test_role_checker_blocks_wrong_role():
    from fastapi import HTTPException

    checker = RoleCheker([Role.ADMIN, Role.MODERATOR])

    fake_regular_user = MagicMock()
    fake_regular_user.role = Role.USER

    with pytest.raises(HTTPException) as exc_info:
        await checker(current_user=fake_regular_user)

    assert exc_info.value.status_code == 403

