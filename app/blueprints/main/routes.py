from flask import render_template, request, flash
import requests
from .forms import PokeLookupForm
from flask_login import login_required
from .import bp as main

@main.route("/", methods=["GET"])
def index():
    return render_template("index.html.j2")

@main.route("/lookup", methods=["GET", "POST"])
@login_required
def lookup():
    form = PokeLookupForm()
    if request.method == "POST":
        pokemon = form.poke_name.data.lower()
        url_base = f"https://pokeapi.co/api/v2/pokemon/{pokemon}"
        response_base = requests.get(url_base)
        if not response_base.ok:
            flash("There was an error, most likely because the Pokemon you entered does not exist. Please try again.", "danger")
            return render_template("lookup.html.j2", form=form)
        if not response_base.json():
            flash("There was an unexpected error. Please try again.", "danger")
            return render_template("lookup.html.j2", form=form)
        poke_data = response_base.json()
        inches = round(poke_data["height"] * 3.937)
        pokemon_dict = {
            "name": poke_data["species"]["name"],
            "id": poke_data["id"],
            "height": f"{str(int(inches//12))}' {str(int(inches%12))}\"",
            "sprite": poke_data["sprites"]["other"]["home"]["front_default"],
            "base_experience": poke_data["base_experience"],
            "ability_name": poke_data["abilities"][0]["ability"]["name"],
            "attack_base": poke_data["stats"][1]["base_stat"],
            "hp_base": poke_data["stats"][0]["base_stat"],
            "defense_base":poke_data["stats"][2]["base_stat"],
        }
        return render_template("lookup.html.j2", pokemon_table=pokemon_dict, form=form)
    return render_template("lookup.html.j2", form=form)
