# ===================================================
# app/chat.py
# Part 1
# ===================================================

from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash,
    request
)

from flask_login import (
    login_required,
    current_user
)

from app import db,socketio

from app.models import (
    User,
    GroupMessage,
    PrivateMessage,
    AIChatHistory,
    Notification
)

from app.forms import (
    GroupMessageForm,
    PrivateMessageForm,
    SearchForm,
    AIChatForm
)

from app.utils import (
    save_chat_image,
    save_chat_file
)

from app.ai import get_ai_response


# ===================================================
# Blueprint
# ===================================================

chat = Blueprint(
    "chat",
    __name__
)


# ===================================================
# Group Chat
# ===================================================

@chat.route(
    "/group-chat",
    methods=["GET", "POST"]
)
@login_required
def group_chat():

    form = GroupMessageForm()

    # ---------------------------------------
    # Send Message
    # ---------------------------------------

    if form.validate_on_submit():

        image_name = None
        file_name = None

        # Upload Image
        if form.image.data:
            image_name = save_chat_image(
                form.image.data
            )

        # Upload File
        if form.file.data:
            file_name = save_chat_file(
                form.file.data
            )

        # Save Message

        message = GroupMessage(
            sender_id=current_user.id,
            message=form.message.data,
            image=image_name,
            file=file_name
        )

        db.session.add(message)
        db.session.commit()

        flash(
            "Message sent successfully.",
            "success"
        )

        return redirect(
            url_for("chat.group_chat")
        )

    # ---------------------------------------
    # Load Messages
    # ---------------------------------------

    messages = (
        GroupMessage.query
        .filter_by(is_deleted=False)
        .order_by(GroupMessage.created_at.asc())
        .all()
    )

    return render_template(
        "group_chat.html",
        form=form,
        messages=messages
    )

# ===================================================
# Private Chat
# ===================================================

@chat.route(
    "/private-chat/<int:user_id>",
    methods=["GET", "POST"]
)
@login_required
def private_chat(user_id):

    receiver = User.query.get_or_404(user_id)

    # ---------------------------------------
    # Prevent chatting with yourself
    # ---------------------------------------

    if receiver.id == current_user.id:

        flash(
            "You cannot chat with yourself.",
            "warning"
        )

        return redirect(
            url_for("main.dashboard")
        )

    form = PrivateMessageForm()

    # ---------------------------------------
    # Send Message
    # ---------------------------------------

    if form.validate_on_submit():

        image_name = None
        file_name = None

        # Upload Image

        if form.image.data:

            image_name = save_chat_image(
                form.image.data
            )

        # Upload File

        if form.file.data:

            file_name = save_chat_file(
                form.file.data
            )

        # Save Message
# -------------------------------
        message = PrivateMessage(

            sender_id=current_user.id,

            receiver_id=receiver.id,

            message=form.message.data,

            image=image_name,

            file=file_name

        )

        db.session.add(message)
# -----------------------------
# Create Notification
# -----------------------------
        notification = Notification(
            sender_id=current_user.id,
            receiver_id=receiver.id,
            message=f"{current_user.username} sent you a message.",
           
        )
        db.session.add(notification)
        db.session.commit()

        socketio.emit(
            "new_private_message",
            {
              "message_id": message.id,
              "sender_id": current_user.id,
              "receiver_id": receiver.id,
              "sender": current_user.username,
              "message": message.message,
              "time": message.created_at.strftime("%I:%M %p")
                
            },
            room=f"user_{receiver.id}"
        )
    #     # Real-time notification
    #     socketio.emit(
    #         "new_notification",
    #         {
    #            "id": notification.id,
    #            "message": notification.message,
    #            "sender_id": current_user.id
    #        },
    #         room=f"user_{receiver.id}"
    #   )
        return redirect(
            url_for(
            "chat.private_chat",
            user_id=receiver.id
            )
     )

    # ---------------------------------------
    # Conversation
    # ---------------------------------------

    messages = (

        PrivateMessage.query.filter(

            (
                (PrivateMessage.sender_id == current_user.id)
                &
                (PrivateMessage.receiver_id == receiver.id)
            )

            |

            (
                (PrivateMessage.sender_id == receiver.id)
                &
                (PrivateMessage.receiver_id == current_user.id)
            )

        )

        .filter_by(is_deleted=False)

        .order_by(
            PrivateMessage.created_at.asc()
        )

        .all()

    )

    # ---------------------------------------
    # Mark Messages as Read
    # ---------------------------------------

    unread_messages = (

        PrivateMessage.query.filter_by(

            sender_id=receiver.id,

            receiver_id=current_user.id,

            is_read=False,

            is_deleted=False

        ).all()

    )

    if unread_messages:

        for msg in unread_messages:

            msg.is_read = True

        db.session.commit()

    # ---------------------------------------
    # Render Page
    # ---------------------------------------

    return render_template(

        "private_chat.html",

        receiver=receiver,

        form=form,

        messages=messages

    )

# ===================================================
# Search Users
# ===================================================

@chat.route(
    "/search",
    methods=["GET", "POST"]
)
@login_required
def search_users():

    form = SearchForm()

    users = []

    if form.validate_on_submit():

        keyword = form.search.data.strip()

        users = (

            User.query.filter(

                User.username.ilike(f"%{keyword}%")

            )

            .filter(

                User.id != current_user.id

            )

            .order_by(

                User.username.asc()

            )

            .all()

        )

        if not users:

            flash(
                "No users found.",
                "warning"
            )

    return render_template(

        "search.html",

        form=form,

        users=users

    )


# ===================================================
# User Profile (View Other User)
# ===================================================

@chat.route("/user/<int:user_id>")
@login_required
def user_profile(user_id):

    user = User.query.get_or_404(user_id)

    return render_template(
        "user_profile.html",
        user=user
    )


# ===================================================
# AI Chat
# ===================================================

@chat.route(
    "/ai-chat",
    methods=["GET", "POST"]
)
@login_required
def ai_chat():

    form = AIChatForm()

    # ---------------------------------------
    # Ask AI
    # ---------------------------------------

    if form.validate_on_submit():

        question = form.question.data.strip()

        answer = get_ai_response(question)

        history = AIChatHistory(

            user_id=current_user.id,

            question=question,

            answer=answer

        )

        db.session.add(history)

        db.session.commit()

        flash(
            "AI response generated successfully.",
            "success"
        )

        return redirect(
            url_for("chat.ai_chat")
        )

    # ---------------------------------------
    # Chat History
    # ---------------------------------------

    history = (

        AIChatHistory.query

        .filter_by(

            user_id=current_user.id

        )

        .order_by(

            AIChatHistory.created_at.desc()

        )

        .all()

    )

    return render_template(

        "ai_chat.html",

        form=form,

        history=history

    )

# ===================================================
# Delete Group Message
# ===================================================

@chat.route("/delete-message/<int:message_id>")
@login_required
def delete_message(message_id):

    message = PrivateMessage.query.get_or_404(message_id)

    if message.sender_id != current_user.id:

        flash(
            "You are not allowed to delete this message.",
            "danger"
        )

        return redirect(
            url_for(
                "chat.private_chat",
                user_id=message.sender_id
            )
        )

    receiver_id = message.receiver_id

    message.is_deleted = True

    db.session.commit()

    flash(
        "Message deleted successfully.",
        "success"
    )

    return redirect(
        url_for(
            "chat.private_chat",
            user_id=receiver_id
        )
    )