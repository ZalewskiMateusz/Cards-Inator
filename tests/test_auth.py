import sys
import os

# Dodaj folder projektu do ścieżki systemowej
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from app import app
from db import get_db_connection
from werkzeug.security import generate_password_hash

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture(autouse=True)
def clean_db():
    """Czyści bazę danych przed każdym testem."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE username IN ('testuser', 'existinguser') OR email IN ('test@example.com', 'existing@example.com')")
    conn.commit()
    cursor.close()
    conn.close()

def test_register_success(client):
    response = client.post('/register', data={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'password123',
        'confirm_password': 'password123'
    }, follow_redirects=True)
    assert b'Registration completed successfully' in response.data

def test_register_username_exists(client):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)", ('existinguser', 'existing@example.com', generate_password_hash('password123')))
    conn.commit()
    cursor.close()
    conn.close()
    response = client.post('/register', data={
        'username': 'existinguser',
        'email': 'test@example.com',
        'password': 'password123',
        'confirm_password': 'password123'
    }, follow_redirects=True)
    assert b'User with this name already exists' in response.data

def test_register_email_exists(client):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)", ('existinguser', 'existing@example.com', generate_password_hash('password123')))
    conn.commit()
    cursor.close()
    conn.close()

    response = client.post('/register', data={
        'username': 'testuser',
        'email': 'existing@example.com',
        'password': 'password123',
        'confirm_password': 'password123'
    }, follow_redirects=True)
    assert b'User with this email already exists' in response.data

def test_register_passwords_not_match(client):
    response = client.post('/register', data={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'password123',
        'confirm_password': 'password456'
    }, follow_redirects=True)
    assert b'Passwords are not the same' in response.data

def test_register_invalid_email(client):
    response = client.post('/register', data={
        'username': 'testuser',
        'email': 'invalid_email',
        'password': 'password123',
        'confirm_password': 'password123'
    }, follow_redirects=True)
    assert b'Invalid email address' in response.data

def test_login_success(client):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)", ('testuser', 'test@example.com', generate_password_hash('password123')))
    conn.commit()
    cursor.close()
    conn.close()

    response = client.post('/login', data={
        'username': 'testuser',
        'password': 'password123'
    }, follow_redirects=True)
    assert b'Logout' in response.data

def test_login_failed(client):
    response = client.post('/login', data={
        'username': 'testuser',
        'password': 'wrongpassword'
    }, follow_redirects=True)
    assert b'Wrong username or password' in response.data
