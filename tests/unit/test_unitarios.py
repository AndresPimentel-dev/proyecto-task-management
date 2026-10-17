from unittest.mock import MagicMock

from app.auth import (
    create_access_token,
    decode_token,
    get_current_user,
    get_password_hash,
    verify_password,
)


def test_generate_hash():
    plain_password = "test password"
    hashed = get_password_hash(plain_password)

    assert plain_password != hashed
    assert hashed is not None
    assert isinstance(hashed, str)


def test_verify_password():
    plain_password = "test password"
    hashed = get_password_hash(plain_password)
    verify = verify_password(plain_password, hashed)

    assert isinstance(verify, bool)
    assert verify is True


def test_verify_incorrect_password():
    plain_password = "test password"
    hashed = get_password_hash(plain_password)
    verify = verify_password("otherpassword", hashed)

    assert isinstance(verify, bool)
    assert verify is False


def test_create_token():
    data = {"sub": "username"}
    token = create_access_token(data)

    assert isinstance(token, str)
    assert token is not None


def test_verify_token():
    mock_db = MagicMock()
    mock_db.query.return_value.filter.return_value.first.return_value = {
        "username": "fakeusername",
        "email": "fakeemail",
    }
    data = {"sub": "username"}
    token = create_access_token(data)
    verficar_token = get_current_user(token, mock_db)

    assert verficar_token == {"username": "fakeusername", "email": "fakeemail"}
    assert verficar_token is not None


def test_decode_token():
    data = {"sub": "username"}
    token = create_access_token(data)
    decoded_token = decode_token(token)

    assert isinstance(decoded_token, str)
    assert decoded_token == "username"


def test_decode_invalid_token():
    invalid_token = "invalidtoken"
    decoded_token = decode_token(invalid_token)

    assert decoded_token is None


def test_get_current():
    mock_db = MagicMock()
    mock_user = {"username": "fakeusername", "email": "fakeemail"}
    mock_db.query.return_value.filter.return_value.first.return_value = mock_user
    data = {"sub": "username"}
    token = create_access_token(data)
    current_user = get_current_user(token, mock_db)

    assert current_user == mock_user
    assert current_user is not None
