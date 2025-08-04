from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os



# Creating Database
db = SQLAlchemy()

# Creating a Function which will create the Flask Object 'app' and it's configuration and imports and connection with DB
def create_app():
    app = Flask(__name__)

    
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "fallback_secret")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///todo.db")

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # SQLAlchemy Database connection with the flask object 'app'
    db.__init__(app)

    from app.routes.auth import auth_bp
    from app.routes.tasks import task_bp
    from app.routes.registration import registration_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(task_bp)
    app.register_blueprint(registration_bp)

    return app 