from flask import render_template, request, flash, redirect, url_for
import requests
from .forms import PokeLookupForm, RegisterForm
from app import app
from .models import User


@app.route("/", methods=["GET"])
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
        flash("You have successfully registered. You may now use the Pokedex!", "success")
        return redirect(url_for("login"))
    return render_template("register.html.j2", form=form)


# @app.route("/login", methods=["GET", "POST"])
# def login():
#     pass

@app.route("/lookup", methods=["GET", "POST"])
def lookup():
    form = PokeLookupForm()
    if request.method == "POST":
        pokemon = form.poke_name.data.lower()
        url = f"https://pokeapi.co/api/v2/pokemon/{pokemon}"
        response = requests.get(url)
        if not response.ok:
            error_string = "There was an error. Please try again."
            return render_template("lookup.html.j2", error=error_string, form=form)
        if not response.json():
            error_string = "There was an error, most likely because the Pokemon you entered does not exist. Please try again."
            return render_template("lookup.html.j2", error=error_string, form=form)
        poke_data = response.json()
        pokemon_dict = {
            "name": poke_data["species"]["name"],
            "sprite": poke_data["sprites"]["front_shiny"],
            "base_experience": poke_data["base_experience"],
            "ability_name": poke_data["abilities"][0]["ability"]["name"],
            "attack_base": poke_data["stats"][1]["base_stat"],
            "hp_base": poke_data["stats"][0]["base_stat"],
            "defense_base":poke_data["stats"][2]["base_stat"],
        }
        return render_template("lookup.html.j2", pokemon_table=pokemon_dict, form=form)
    return render_template("lookup.html.j2", form=form)