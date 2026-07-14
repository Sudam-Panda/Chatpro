# ===================================================
# app/routes.py
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

from app import db

from app.models import (
    User,
    Notification
)


# ===================================================
# Blueprint
# ===================================================

main = Blueprint(
    "main",
    __name__
)


# ===================================================
# Home Page
# ===================================================

@main.route("/")
def home():

    return render_template(
        "index.html"
    )


# ===================================================
# Dashboard
# ===================================================

@main.route("/dashboard")
@login_required
def dashboard():

    users = User.query.filter(
        User.id != current_user.id
    ).order_by(
        User.username.asc()
    ).all()

    return render_template(
        "dashboard.html",
        users=users
    )


# ===================================================
# Notifications
# ===================================================

@main.route("/notifications")
@login_required
def notifications():

    notifications = Notification.query.filter_by(
        receiver_id=current_user.id
    ).order_by(
        Notification.created_at.desc()
    ).all()

    return render_template(
        "notifications.html",
        notifications=notifications
    )


# ===================================================
# Read Notification
# ===================================================

@main.route("/read-notification/<int:id>")
@login_required
def read_notification(id):

    notification = Notification.query.get_or_404(id)

    if notification.receiver_id != current_user.id:

        return redirect(
            url_for("main.notifications")
        )

    notification.is_read = True

    db.session.commit()

    return redirect(
        url_for(
            "chat.private_chat",
            user_id=notification.sender_id
        )
    )


# ===================================================
# Mark All Notifications Read
# ===================================================

@main.route("/mark-all-read")
@login_required
def mark_all_read():

    Notification.query.filter_by(
        receiver_id=current_user.id,
        is_read=False
    ).update(
        {
            "is_read": True
        }
    )

    db.session.commit()

    return redirect(
        url_for(
            "main.notifications"
        )
    )


# ===================================================
# All Users
# ===================================================
@main.route("/users")
@login_required
def users():

    search = request.args.get("q", "").strip()

    if search:

        users = User.query.filter(
            User.username.ilike(f"%{search}%"),
            User.id != current_user.id
        ).order_by(
            User.username.asc()
        ).all()

    else:

        users = User.query.filter(
            User.id != current_user.id
        ).order_by(
            User.username.asc()
        ).all()

    return render_template(
        "search.html",
        users=users
    )


# ===================================================
# About Page
# ===================================================

@main.route("/about")
def about():

    return render_template(
        "about.html"
    )


# ===================================================
# Contact Page
# ===================================================

@main.route("/contact")
def contact():

    return render_template(
        "contact.html"
    )


# ===================================================
# Error Pages
# ===================================================

@main.app_errorhandler(404)
def page_not_found(error):

    return render_template(
        "errors/404.html"
    ), 404


@main.app_errorhandler(500)
def internal_server_error(error):

    return render_template(
        "errors/500.html"
    ), 500

# ===================================================
# Clear All Notifications
# ===================================================

@main.route("/clear-notifications")
@login_required
def clear_notifications():

    Notification.query.filter_by(
        receiver_id=current_user.id
    ).delete()

    db.session.commit()

    flash(
        "All notifications cleared successfully.",
        "success"
    )

    return redirect(
        url_for("main.notifications")
    )