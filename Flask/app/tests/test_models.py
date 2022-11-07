from app import *
from app.models import User
import pytest

@pytest.fixture
def my_user1():
    my_user1 = User(first_name="Rudy", last_name='Bourez', email="admin@example.com", password="1234")
    return my_user1

@pytest.fixture
def my_user2():
    my_user2 = User(first_name="User", last_name="User", email="user@example.com", password="123456")
    return my_user2


def test_models(my_user1, my_user2):
    assert my_user1.first_name == "Rudy"
    assert my_user1.last_name == "Bourez"
    assert my_user2.first_name == "User"
    assert my_user2.last_name == "User"