from flask import Flask
from auth import auth_bp, init_auth, login_manager
from routes import routes_bp
import os
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

# Rejestracja blueprintów
app.register_blueprint(auth_bp)
init_auth(app, login_manager)
app.register_blueprint(routes_bp)

if __name__ == '__main__':
    app.run(debug=True)
