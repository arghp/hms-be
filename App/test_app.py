import pytest
from unittest.mock import patch

from werkzeug.security import generate_password_hash

from App import app
from App.Models.models import User, Room
from App.config import db

@pytest.fixture
def test_client():
    with app.app_context():
        # Set up the database
        db.create_all()

        # Create test data
        test_user = User(username='test', password_hash=generate_password_hash('test'), email='test@example.com', first_name='Test', last_name='test')
        db.session.add(test_user)

        test_room_1 = Room(room_type='Standard', room_price=100, status='Available')
        test_room_2 = Room(room_type='Deluxe', room_price=200, status='Available')
        db.session.add(test_room_1)
        db.session.add(test_room_2)

        db.session.commit()

        # Push the application context
        ctx = app.app_context()
        ctx.push()

        yield app.test_client()

        # Pop the application context
        ctx.pop()

        # Teardown the database
        db.session.remove()
        db.drop_all()


@patch('App.Models.models.User')
def test_login(mock_user, test_client):
    mock_user.query.filter_by.return_value.first.return_value = mock_user(
        username='test2',
        password_hash='hashed_password'
    )

    response = test_client.post('/login', data=dict(username='test', password='test'), follow_redirects=True)
    print(f"Expected status code: 200. Got: {response.status_code}")
    print(f"Expected 'Logged in successfully.' in response.data. Got: {b'Logged in successfully.' in response.data}")


@patch('App.Models.models.Room')
def test_get_rooms(mock_room, test_client):
    mock_room.query.all.return_value = [
        mock_room(room_id=1, room_type='Standard', room_price=100, status='Available'),
        mock_room(room_id=2, room_type='Deluxe', room_price=200, status='Available')
    ]

    response = test_client.get('/rooms')
    data = response.get_json()

    print(f"Expected status code: 200. Got: {response.status_code}")
    print(f"Expected data to be a list. Got: {type(data).__name__}")
    print(f"Expected list length: 2. Got: {len(data)}")
    print(f"Expected room_id of first room to be 1. Got: {data[0]['room_id']}")
    print(f"Expected room_id of second room to be 2. Got: {data[1]['room_id']}")


@patch('App.Models.models.User')
def test_register(mock_user, test_client):
    mock_user.query.filter_by.return_value.first.return_value = None

    response = test_client.post('/register', data=dict(
        username='testuser',
        password='testpass',
        email='testuser@example.com',
        first_name='Test',
        last_name='User'
    ))

    print(f"Expected status code: 201. Got: {response.status_code}")

    # Instead of checking the mock user, retrieve the user from the database
    user = User.query.filter_by(username='testuser').first()
    print(f"Expected user to exist. Got: {user is not None}")
    print(f"Expected username to be 'testuser'. Got: {user.username}")
    print(f"Expected password to be hashed. Got: {user.password_hash != 'testpass'}")

    response = test_client.post('/register', data=dict(
        username='testuser',
        password='testpass',
        email='testuser@example.com',
        first_name='Test',
        last_name='User'
    ))

    print(f"Expected status code: 409. Got: {response.status_code}")

