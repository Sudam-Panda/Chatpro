from datetime import datetime
from zoneinfo import ZoneInfo

from flask_login import UserMixin

from app import db, login_manager, bcrypt

# ===================================================
# Indian Standard Time
# ===================================================

IST = ZoneInfo("Asia/Kolkata")


def ist_now():
    return datetime.now(IST)


# ===================================================
# Flask Login
# ===================================================

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


# ===================================================
# User Model
# ===================================================

class User(UserMixin, db.Model):

    __tablename__ = "users"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    username = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )

    email = db.Column(
        db.String(150),
        unique=True,
        nullable=False
    )

    password_hash = db.Column(
        db.String(255),
        nullable=False
    )

    profile_picture = db.Column(
        db.String(255),
        default="default.png"
    )

    about = db.Column(
        db.Text,
        default=""
    )

    is_online = db.Column(
        db.Boolean,
        default=False
    )

    last_seen = db.Column(
        db.DateTime,
        default=ist_now
    )

    created_at = db.Column(
        db.DateTime,
        default=ist_now
    )

    # -------------------------
    # Relationships
    # -------------------------

    group_messages = db.relationship(
        "GroupMessage",
        backref="sender",
        lazy=True,
        cascade="all, delete-orphan"
    )

    sent_private_messages = db.relationship(
        "PrivateMessage",
        foreign_keys="PrivateMessage.sender_id",
        backref="sender_user",
        lazy=True,
        cascade="all, delete-orphan"
    )

    received_private_messages = db.relationship(
        "PrivateMessage",
        foreign_keys="PrivateMessage.receiver_id",
        backref="receiver_user",
        lazy=True,
        cascade="all, delete-orphan"
    )

    ai_chat_history = db.relationship(
        "AIChatHistory",
        backref="user",
        lazy=True,
        cascade="all, delete-orphan"
    )

    sent_notifications = db.relationship(
        "Notification",
        foreign_keys="Notification.sender_id",
        backref="sender",
        lazy=True,
        cascade="all, delete-orphan"
    )

    received_notifications = db.relationship(
        "Notification",
        foreign_keys="Notification.receiver_id",
        backref="receiver",
        lazy=True,
        cascade="all, delete-orphan"
    )

    # -------------------------
    # Password
    # -------------------------

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(
            password
        ).decode("utf-8")

    def check_password(self, password):
        return bcrypt.check_password_hash(
            self.password_hash,
            password
        )

    def update_last_seen(self):
        self.last_seen = ist_now()
        db.session.commit()

    def __repr__(self):
        return f"<User {self.username}>"


# ===================================================
# Group Message Model
# ===================================================

class GroupMessage(db.Model):

    __tablename__ = "group_messages"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    sender_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    message = db.Column(
        db.Text
    )

    image = db.Column(
        db.String(255)
    )

    file = db.Column(
        db.String(255)
    )

    is_read = db.Column(
        db.Boolean,
        default=False
    )

    is_deleted = db.Column(
        db.Boolean,
        default=False,
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=ist_now
    )

    def to_dict(self):
        return {
            "id": self.id,
            "sender_id": self.sender_id,
            "sender": self.sender.username if self.sender else "",
            "message": self.message,
            "image": self.image,
            "file": self.file,
            "is_read": self.is_read,
            "created_at": self.created_at.strftime("%d-%m-%Y %I:%M %p")
        }

    def __repr__(self):
        return f"<GroupMessage {self.id}>"


# ===================================================
# Private Message Model
# ===================================================

class PrivateMessage(db.Model):

    __tablename__ = "private_messages"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    sender_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    receiver_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    message = db.Column(
        db.Text
    )

    image = db.Column(
        db.String(255)
    )

    file = db.Column(
        db.String(255)
    )

    is_read = db.Column(
        db.Boolean,
        default=False,
        nullable=False
    )

    is_deleted = db.Column(
        db.Boolean,
        default=False,
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=ist_now,
        nullable=False
    )

    def mark_as_read(self):
        self.is_read = True

    def to_dict(self):
        return {
            "id": self.id,
            "sender_id": self.sender_id,
            "receiver_id": self.receiver_id,
            "sender": self.sender_user.username if self.sender_user else "",
            "receiver": self.receiver_user.username if self.receiver_user else "",
            "message": self.message,
            "image": self.image,
            "file": self.file,
            "is_read": self.is_read,
            "created_at": self.created_at.strftime("%d-%m-%Y %I:%M %p")
        }

    def __repr__(self):
        return f"<PrivateMessage {self.sender_id}->{self.receiver_id}>"


# ===================================================
# AI Chat History
# ===================================================

class AIChatHistory(db.Model):

    __tablename__ = "ai_chat_history"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    question = db.Column(
        db.Text,
        nullable=False
    )

    answer = db.Column(
        db.Text,
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=ist_now,
        nullable=False
    )

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "question": self.question,
            "answer": self.answer,
            "created_at": self.created_at.strftime("%d-%m-%Y %I:%M %p")
        }

    def __repr__(self):
        return f"<AIChatHistory {self.id}>"


# ===================================================
# Notification Model
# ===================================================

class Notification(db.Model):

    __tablename__ = "notifications"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    sender_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    receiver_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    message = db.Column(
        db.String(255),
        nullable=False
    )

    link = db.Column(
        db.String(255),
        nullable=True
    )

    is_read = db.Column(
        db.Boolean,
        default=False,
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=ist_now,
        nullable=False
    )

    def __repr__(self):
        return f"<Notification {self.id}>"
    
class SearchHistory(db.Model):

    __tablename__ = "search_history"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    searched_user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=ist_now
    )