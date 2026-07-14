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

from app.forms import ProfileForm

from app.utils import save_profile_picture


# ===================================================
# Blueprint
# ===================================================

profile = Blueprint(
    "profile",
    __name__
)


# ===================================================
# Profile Page
# ===================================================

@profile.route(
    "/profile",
    methods=["GET", "POST"]
)
@login_required
def user_profile():

    form = ProfileForm()

    if form.validate_on_submit():

        # Update Username
        current_user.username = form.username.data

        # Update About
        current_user.about = form.about.data

        # Upload Profile Picture
        if form.profile_picture.data:

            picture_file = save_profile_picture(
                form.profile_picture.data
            )

            if picture_file:
                current_user.profile_picture = picture_file

        db.session.commit()

        flash(
            "Profile updated successfully.",
            "success"
        )

        return redirect(
            url_for("profile.user_profile")
        )

    elif request.method == "GET":

        form.username.data = current_user.username
        form.about.data = current_user.about

    return render_template(
        "profile.html",
        form=form,
        user=current_user
    )