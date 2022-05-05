from flask import render_template, request, flash, redirect, url_for
import requests
from .forms import PokeLookupForm, RegisterForm, LoginForm
from app import app
from .models import User
from flask_login import login_required, login_user, current_user, logout_user

@app.route("/", methods=["GET"])
@login_required
def index():
    return render_template("index.html.j2")

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if request.method == "POST" and form.validate_on_submit():
        try:
            new_user_data = {
                "first_name": form.first_name.data.title(),
                "last_name": form.last_name.data.title(),
                "email": form.email.data.lower(),
                "password": form.password.data,
            }
            new_user_object = User()
            new_user_object.form_to_db(new_user_data)
            new_user_object.save()
        except:
            flash("There was an unexpected error creating your account. Please try again later.", "danger")
            return render_template("register.html.j2", form=form)
        flash("You have successfully registered. Please login to use the Pokedex!", "success")
        return redirect(url_for("login"))
    return render_template("register.html.j2", form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if request.method == "POST" and form.validate_on_submit():
        email = form.email.data.lower()
        password = form.password.data
        user = User.query.filter_by(email=email).first()
        if user and user.confirm_password(password):
            login_user(user)
            flash("Login successful. You may now use the Pokedex!", "success")
            return redirect(url_for("index"))
        flash("Incorrect email or password.", "danger")
        return render_template("login.html.j2", form=form)
    return render_template("login.html.j2", form=form)

@app.route("/lookup", methods=["GET", "POST"])
@login_required
def lookup():
    form = PokeLookupForm()
    if request.method == "POST":
        pokemon = form.poke_name.data.lower()
        url = f"https://pokeapi.co/api/v2/pokemon/{pokemon}"
        response = requests.get(url)
        if not response.ok:
            flash("There was an error, most likely because the Pokemon you entered does not exist. Please try again.", "danger")
            return render_template("lookup.html.j2", form=form)
        if not response.json():
            flash("There was an unexpected error. Please try again.", "danger")
            return render_template("lookup.html.j2", form=form)
        poke_data = response.json()
        pokemon_dict = {
            "name": poke_data["species"]["name"],
            "sprite": poke_data["sprites"]["other"]["home"]["front_default"],
            "base_experience": poke_data["base_experience"],
            "ability_name": poke_data["abilities"][0]["ability"]["name"],
            "attack_base": poke_data["stats"][1]["base_stat"],
            "hp_base": poke_data["stats"][0]["base_stat"],
            "defense_base":poke_data["stats"][2]["base_stat"],
        }
        return render_template("lookup.html.j2", pokemon_table=pokemon_dict, form=form)
    return render_template("lookup.html.j2", form=form)

@app.route("/logout")
@login_required
def logout():
    if current_user:
        logout_user()
        flash("You have logged out successfully.", "primary")
        return redirect(url_for("login"))