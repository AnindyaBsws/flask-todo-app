from flask import Flask, Blueprint, request, session, flash, render_template, redirect, url_for
from werkzeug.security import check_password_hash
from app.models import User



# Creating the Blueprint Object with internal name 'auth'
auth_bp = Blueprint('auth', __name__)

# Setiing Custom User Credentials
USER_CREDENTIALS = {
    "username" : "Derek",
    "password" : "hola"
}


@auth_bp.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = User.query.filter_by(username = request.form.get("username")).first()
        if user and check_password_hash(user.password, request.form.get("password")):
            session['user'] = user.username
            flash(f"Welcome {user.username}!", "success")
            return redirect(url_for('task.add_task'))
        else:
            flash("Invalid credentials", "error")
        

        # if username == USER_CREDENTIALS["username"] and password == USER_CREDENTIALS["password"]:
        #     session["user"] = username
        #     flash(f"Welcome {session["user"]}, login successfull", "success")
        #     return redirect(url_for("task.view_task"))
        # else:
        #     flash("Invalid Credentials", "error")

    return render_template("login.html")


@auth_bp.route("/home")
def home():
    if "user"  in session:
        flash(f"Welcome {session["user"]}, login successfull", "success")
    else:
        flash("Unexpected Error", "danger")

    return render_template("home.html")


@auth_bp.route('/logout')
def logout():
    # if 'user' not in session:
    #     return render_template("login.html")
    
    session.pop("user", None)
    flash("Successfully Logged Out", "logout")
    return redirect(url_for("auth.login"))


