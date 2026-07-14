import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from flask_bcrypt import Bcrypt
from flask_socketio import SocketIO
from flask_migrate import Migrate

from config import Config


# ===================================================
# Extensions
# ===================================================

db = SQLAlchemy()

bcrypt = Bcrypt()

login_manager = LoginManager()

migrate = Migrate()


socketio = SocketIO(
    cors_allowed_origins="*",
    async_mode="threading"
)


# ===================================================
# Login Config
# ===================================================

login_manager.login_view = "auth.login"

login_manager.login_message = "Please login first."

login_manager.login_message_category = "warning"



# ===================================================
# Create App
# ===================================================

def create_app():

    app = Flask(__name__)

    app.config.from_object(Config)


    # Initialize Extensions

    db.init_app(app)

    bcrypt.init_app(app)

    login_manager.init_app(app)

    migrate.init_app(app, db)

    socketio.init_app(app)



    # ===================================================
    # Create Upload Folders
    # ===================================================

    os.makedirs(
        app.config["UPLOAD_FOLDER"],
        exist_ok=True
    )

    os.makedirs(
        app.config["PROFILE_FOLDER"],
        exist_ok=True
    )

    os.makedirs(
        app.config["IMAGE_FOLDER"],
        exist_ok=True
    )

    os.makedirs(
        app.config["FILE_FOLDER"],
        exist_ok=True
    )



    # Import Models

    from app import models

    from app.models import Notification



    # ===================================================
    # Notification Count
    # Available All Templates
    # ===================================================

    @app.context_processor
    def inject_notification_count():

        if current_user.is_authenticated:

            count = Notification.query.filter_by(
                receiver_id=current_user.id,
                is_read=False
            ).count()

        else:

            count = 0


        return {
            "notification_count": count
        }



    # ===================================================
    # Blueprints
    # ===================================================

    from app.auth import auth

    from app.chat import chat

    from app.profile import profile

    from app.routes import main



    app.register_blueprint(auth)

    app.register_blueprint(chat)

    app.register_blueprint(profile)

    app.register_blueprint(main)



    # ===================================================
    # Socket Events
    # ===================================================

    # Socket Events

    from app import socket_handlers



    # ===================================================
    # Error Handling
    # ===================================================

    @app.errorhandler(404)
    def page_not_found(error):

        return "404 - Page Not Found", 404



    @app.errorhandler(500)
    def internal_server_error(error):

        db.session.rollback()

        return "500 - Internal Server Error", 500



    return app