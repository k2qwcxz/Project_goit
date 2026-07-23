import pytest
from PhotoShare.services.auth import auth_service


def test_password_hash_and_very():
    password = "qweqwe123"
    hashed = auth_service.get_password_hash(password)

    assert hashed != password
    assert auth_service.verify_password(password, hashed) is True
    assert auth_service.verify_password("wrongpasword", hashed) is False




    