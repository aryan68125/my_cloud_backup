import hashlib

import pytest

from auth.auth_handler import (
    create_access_token,
    create_refresh_token,
    hash_password,
    verify_access_token,
    verify_password,
)
from fastapi import HTTPException


def test_hash_password_produces_different_hash_each_time():
    h1 = hash_password("mysecret")
    h2 = hash_password("mysecret")
    assert h1 != h2


def test_verify_password_correct():
    hashed = hash_password("mysecret")
    assert verify_password("mysecret", hashed) is True


def test_verify_password_wrong():
    hashed = hash_password("mysecret")
    assert verify_password("wrongpassword", hashed) is False


def test_create_and_verify_access_token():
    token = create_access_token(user_id=1, email="test@example.com")
    payload = verify_access_token(token)
    assert payload["sub"] == "1"
    assert payload["email"] == "test@example.com"
    assert payload["type"] == "access"


def test_verify_access_token_invalid_raises():
    with pytest.raises(HTTPException) as exc_info:
        verify_access_token("not.a.valid.token")
    assert exc_info.value.status_code == 401


def test_create_refresh_token_returns_raw_and_hash():
    raw, hashed = create_refresh_token()
    assert len(raw) > 32
    assert len(hashed) == 64  # SHA-256 hex digest
    assert raw != hashed


def test_refresh_token_raw_and_hash_are_consistent():
    raw, hashed = create_refresh_token()
    expected_hash = hashlib.sha256(raw.encode()).hexdigest()
    assert hashed == expected_hash
