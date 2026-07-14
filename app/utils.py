import os
import secrets

from PIL import Image

from werkzeug.utils import secure_filename

from flask import current_app


# ===================================================
# Allowed Extensions
# ===================================================

IMAGE_EXTENSIONS = {
    "png",
    "jpg",
    "jpeg",
    "gif"
}


FILE_EXTENSIONS = {
    "pdf",
    "doc",
    "docx",
    "txt",
    "zip"
}


# ===================================================
# Check File Extension
# ===================================================

def allowed_file(filename, allowed_extensions):

    return (
        "." in filename
        and
        filename.rsplit(".", 1)[1].lower()
        in allowed_extensions
    )


# ===================================================
# Save Profile Picture
# ===================================================

def save_profile_picture(uploaded_file):

    if not uploaded_file:
        return None


    if not allowed_file(
        uploaded_file.filename,
        IMAGE_EXTENSIONS
    ):
        return None


    random_hex = secrets.token_hex(8)


    _, extension = os.path.splitext(
        secure_filename(
            uploaded_file.filename
        )
    )


    filename = random_hex + extension


    save_path = os.path.join(
        current_app.config["PROFILE_FOLDER"],
        filename
    )


    try:

        image = Image.open(
            uploaded_file
        )

        image.thumbnail(
            (300,300)
        )

        image.save(
            save_path
        )


    except Exception as error:

        print(
            "Profile image error:",
            error
        )

        return None


    return filename



# ===================================================
# Save Chat Image
# ===================================================

def save_chat_image(uploaded_file):

    if not uploaded_file:
        return None


    if not allowed_file(
        uploaded_file.filename,
        IMAGE_EXTENSIONS
    ):
        return None


    random_hex = secrets.token_hex(8)


    _, extension = os.path.splitext(
        secure_filename(
            uploaded_file.filename
        )
    )


    filename = random_hex + extension


    save_path = os.path.join(
        current_app.config["IMAGE_FOLDER"],
        filename
    )


    uploaded_file.save(
        save_path
    )


    return filename



# ===================================================
# Save Chat File
# ===================================================

def save_chat_file(uploaded_file):

    if not uploaded_file:
        return None


    if not allowed_file(
        uploaded_file.filename,
        FILE_EXTENSIONS
    ):
        return None


    random_hex = secrets.token_hex(8)


    _, extension = os.path.splitext(
        secure_filename(
            uploaded_file.filename
        )
    )


    filename = random_hex + extension


    save_path = os.path.join(
        current_app.config["FILE_FOLDER"],
        filename
    )


    uploaded_file.save(
        save_path
    )


    return filename