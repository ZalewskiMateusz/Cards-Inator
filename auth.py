from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector
import validators
from db import get_db_connection
import re

auth_bp = Blueprint('auth', __name__)

login_manager = LoginManager()
login_manager.login_view = 'auth.login'


class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password


@login_manager.user_loader
def load_user(user_id):
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        if user:
            return User(user[0], user[1], user[2])
    return None


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
            user = cursor.fetchone()
            cursor.close()
            conn.close()
            if user and check_password_hash(user[2], password):
                user_obj = User(user[0], user[1], user[2])
                login_user(user_obj, remember=True) # Remember on True, should not logout user
                return redirect(url_for('routes.index'))
            else:
                flash('Incorrect username or password')
    return render_template('login.html')


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            flash('Invalid email address')
            return redirect(url_for('auth.register'))

        if password != confirm_password:
            flash('Passwords are not the same')
            return redirect(url_for('auth.register'))

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()

        if user:
            flash('User with this username already exists')
            return redirect(url_for('auth.register'))

        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()

        if user:
            flash('User with this email already exists')
            return redirect(url_for('auth.register'))

        hashed_password = generate_password_hash(password)
        cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)", (username, email, hashed_password))
        conn.commit()
        conn.close()
        flash('Registration completed successfully')
        return redirect(url_for('auth.login'))

    return render_template('register.html')


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have successfully logout')
    return redirect(url_for('auth.login'))

def init_auth(app, login_manager):
    login_manager.init_app(app)
