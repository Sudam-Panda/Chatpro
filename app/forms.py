from flask_wtf import FlaskForm
from flask_wtf.file import FileField

from wtforms import (
    StringField,
    PasswordField,
    SubmitField
)

from wtforms.validators import (
    DataRequired,
    Email,
    Length,
    EqualTo
)


# ==================================
# Register Form
# ==================================

class RegisterForm(FlaskForm):

    username = StringField(
        "Username",
        validators=[
            DataRequired(),
            Length(min=3, max=100)
        ]
    )

    email = StringField(
        "Email",
        validators=[
            DataRequired(),
            Email()
        ]
    )

    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            Length(min=6)
        ]
    )

    confirm_password = PasswordField(
        "Confirm Password",
        validators=[
            DataRequired(),
            EqualTo("password")
        ]
    )

    submit = SubmitField("Register")


# ==================================
# Login Form
# ==================================

class LoginForm(FlaskForm):

    email = StringField(
        "Email",
        validators=[
            DataRequired(),
            Email()
        ]
    )

    password = PasswordField(
        "Password",
        validators=[
            DataRequired()
        ]
    )

    submit = SubmitField("Login")


# ==================================
# Group Message Form
# ==================================

class GroupMessageForm(FlaskForm):

    message = StringField(
        "Message",
        validators=[
            DataRequired(),
            Length(max=500)
        ]
    )

    image = FileField("Image")

    file = FileField("File")

    submit = SubmitField("Send")


# ==================================
# Private Message Form
# ==================================

class PrivateMessageForm(FlaskForm):

    message = StringField(
        "Message",
        validators=[
            DataRequired(),
            Length(max=500)
        ]
    )

    image = FileField("Image")

    file = FileField("File")

    submit = SubmitField("Send")


# ==================================
# Search User Form
# ==================================

class SearchForm(FlaskForm):

    search = StringField(
        "Search User",
        validators=[
            DataRequired(),
            Length(min=2, max=100)
        ]
    )

    submit = SubmitField("Search")


# ==================================
# AI Chat Form
# ==================================

class AIChatForm(FlaskForm):

    question = StringField(
        "Question",
        validators=[
            DataRequired(),
            Length(min=1, max=500)
        ]
    )

    submit = SubmitField("Ask AI")


# ==================================
# Profile Update Form
# ==================================

class ProfileForm(FlaskForm):

    username = StringField(
        "Username",
        validators=[
            DataRequired(),
            Length(min=3, max=100)
        ]
    )

    about = StringField(
        "About",
        validators=[
            Length(max=500)
        ]
    )

    profile_picture = FileField(
        "Profile Picture"
    )

    submit = SubmitField("Update Profile")