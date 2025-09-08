import pytest
from fastapi import HTTPException

from security import get_current_user


def test_get_current_user_when_not_user():

    with pytest.raises(HTTPException):
        get_current_user({})
