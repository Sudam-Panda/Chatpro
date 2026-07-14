import os
from dotenv import load_dotenv


load_dotenv()


class Config:


    SECRET_KEY = os.environ.get(
        "SECRET_KEY"
    )


    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL"
    )


    SQLALCHEMY_TRACK_MODIFICATIONS = False


    UPLOAD_FOLDER = "app/static/uploads"

    PROFILE_FOLDER = (
        "app/static/uploads/profile"
    )

    IMAGE_FOLDER = (
        "app/static/uploads/images"
    )

    FILE_FOLDER = (
        "app/static/uploads/files"
    )