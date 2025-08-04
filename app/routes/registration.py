from flask import Flask, redirect, session, flash, render_template, Blueprint, request, url_for
from werkzeug.security import generate_password_hash
from app.models import User
from app import db


# Creating the Blueprint Object with internal name 'auth'
registration_bp = Blueprint('registration',__name__)


@registration_bp.route('/')
def redirect_url():
    return redirect(url_for("registration.sign_up"))

@registration_bp.route("/signup", methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        username = request.form.get("username").strip()
        password = request.form.get("password").strip()

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash("The Username is already taken")
            return redirect(url_for("registration.sign_up"))

        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        session["user"] = username
        flash(f"Welcome {session["user"]}!, Let's Begin your journey by adding your first task")
        return redirect(url_for("task.add_task"))
    
    return render_template("registration.html")
