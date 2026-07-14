from flask_socketio import (
    emit,
    join_room,
    leave_room
)

from flask_login import current_user

from app import socketio, db



# =========================================
# Connect
# =========================================

@socketio.on("connect")
def handle_connect():

    if current_user.is_authenticated:


        # Join personal notification room
        join_room(
            f"user_{current_user.id}"
        )


        db.session.commit()


        print(
            f"{current_user.username} Online"
        )


        print(
            f"Joined room: user_{current_user.id}"
        )


    else:

        print(
            "Guest Connected"
        )



# =========================================
# Disconnect
# =========================================

@socketio.on("disconnect")
def handle_disconnect():


    if current_user.is_authenticated:


        print(
            f"{current_user.username} Offline"
        )



# =========================================
# Join Group Chat
# =========================================

@socketio.on("join_group")
def join_group():


    join_room(
        "group_chat"
    )


    print(
        f"{current_user.username} joined group"
    )



# =========================================
# Leave Group Chat
# =========================================

@socketio.on("leave_group")
def leave_group():


    leave_room(
        "group_chat"
    )


    print(
        f"{current_user.username} left group"
    )



# =========================================
# Private Chat Room
# =========================================

@socketio.on("join_private")
def join_private(data):


    if not current_user.is_authenticated:

        return



    receiver_id = data.get(
        "receiver_id"
    )


    room = "_".join(
        sorted(
            [
                str(current_user.id),
                str(receiver_id)
            ]
        )
    )


    join_room(room)


    print(
        f"Joined private room {room}"
    )



# =========================================
# Send Real-Time Notification
# =========================================

def send_notification(receiver_id, notification):


    socketio.emit(

        "new_notification",

        {
            "id": notification.id,
            "message": notification.message,
            "sender_id": notification.sender_id
        },

        room=f"user_{receiver_id}"

    )



# =========================================
# Ping
# =========================================

@socketio.on("ping_server")
def ping_server():


    emit(

        "pong_server",

        {
            "message":
            "Server is running"
        }

    )