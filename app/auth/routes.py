"""Routes for authentication and session management."""

from flask import Blueprint, current_app, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

from app.auth.forms import LoginForm
from app import db
from app.audit import log_audit
from app.auth.service import authenticate, available_demo_users


auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    """Log in a foundation administrator or cashier account."""

    if current_user.is_authenticated:
        return redirect(url_for("dashboard.index"))

    form = LoginForm()
    if form.validate_on_submit():
        user = authenticate(form.username.data, form.password.data)
        if user:
            login_user(user)
            log_audit('auth.login','User',user.id,'Successful login')
            db.session.commit()
            flash(f"Welcome, {user.display_name}.", "success")
            next_url = request.args.get("next")
            return redirect(next_url or url_for("dashboard.index"))
        log_audit('auth.login_failed','User',None,f'Failed login for {form.username.data}', severity='WARNING')
        db.session.commit()
        flash("Invalid username or password.", "danger")

    return render_template("auth/login.html", form=form, demo_users=available_demo_users(), show_demo=current_app.debug)


@auth_bp.post("/logout")
@login_required
def logout():
    """Log out the current user."""

    log_audit('auth.logout','User',getattr(current_user,'id',None),'Logout')
    db.session.commit()
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("auth.login"))
