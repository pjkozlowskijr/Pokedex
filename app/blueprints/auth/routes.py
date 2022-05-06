from flask import render_template, request, flash, redirect, url_for
from .forms import RegisterForm, LoginForm, EditProfileForm
from ...models import User
from flask_login import login_required, login_user, current_user, logout_user
from .import bp as auth

@auth.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if request.method == "POST" and form.validate_on_submit():
        try:
            new_user_data = {
                "first_name": form.first_name.data.title(),
                "last_name": form.last_name.data.title(),
                "email": form.email.data.lower(),
                "password": form.password.data,
                "icon": form.icon.data,
            }
            new_user_object = User()
            new_user_object.form_to_db(new_user_data)
            new_user_object.save()
        except:
            flash("There was an unexpected error creating your account. Please try again later.", "danger")
            return render_template("register.html.j2", form=form)
        flash("You have successfully registered. Please login to use the Pokedex!", "success")
        return redirect(url_for("auth.login"))
    return render_template("register.html.j2", form=form)

@auth.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if request.method == "POST" and form.validate_on_submit():
        email = form.email.data.lower()
        password = form.password.data
        user = User.query.filter_by(email=email).first()
        if user and user.confirm_password(password):
            login_user(user)
            flash("Login successful. You may now use the Pokedex!", "success")
            return redirect(url_for("main.index"))
        flash("Incorrect email or password.", "danger")
        return render_template("login.html.j2", form=form)
    return render_template("login.html.j2", form=form)

@auth.route("/edit_profile", methods=["GET", "POST"])
def edit_profile():
    form = EditProfileForm()
    if request.method == "POST" and form.validate_on_submit():
        new_user_data = {
            "first_name": form.first_name.data.title(),
            "last_name": form.last_name.data.title(),
            "email": form.email.data.lower(),
            "password": form.password.data,
            "icon": int(form.icon.data) if int(form.icon.data) != 9000 else current_user.icon,
        }
        user = User.query.filter_by(email=new_user_data["email"]).first()
        if user and user.email != current_user.email:
            flash("Email is already in use.", "danger")
            return redirect(url_for("auth.edit_profile"))
        try:
            current_user.form_to_db(new_user_data)
            current_user.save()
            flash("Your profile was updated successfully.", "success")
        except:
            flash("There was an unexpected error. Please try again.", "danger")
        return redirect(url_for("main.index"))
    return render_template("register.html.j2", form=form)

@auth.route("/logout")
@login_required
def logout():
    if current_user:
        logout_user()
        flash("You have logged out successfully.", "success")
        return redirect(url_for("auth.login"))