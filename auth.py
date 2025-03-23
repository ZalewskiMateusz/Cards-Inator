from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector
import validators
from db import get_db_connection

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

        if password != confirm_password:
            flash('Passwords are not identical')
            return render_template('register.html')

        if not validators.email(email):
            flash('Invalid email address')
            return render_template('register.html')

        hashed_password = generate_password_hash(password)
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            try:
                cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
                               (username, email, hashed_password))
                conn.commit()
                flash('Registration successful, you can log in')
                return redirect(url_for('auth.login'))
            except mysql.connector.IntegrityError as err:
                if 'username' in str(err):
                    flash('User with this name already exists')
                elif 'email' in str(err):
                    flash('User with this email address already exists')
            except mysql.connector.Error as err:
                flash(f'Registration error: {err}')
            finally:
                cursor.close()
                conn.close()
    return render_template('register.html')


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('routes.index'))

def init_auth(app, login_manager):
    login_manager.init_app(app)
