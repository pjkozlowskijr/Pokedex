from flask import render_template, request
import requests
from .forms import PokeLookupForm
from app import app

@app.route("/", methods = ['GET'])
def index():
    return render_template("index.html.j2")

@app.route("/lookup", methods = ['GET', 'POST'])
def lookup():
    form = PokeLookupForm()
    if request.method == "POST":
        pokemon = form.poke_name.data.lower()
        url = f"https://pokeapi.co/api/v2/pokemon/{pokemon}"
        response = requests.get(url)
        if not response.ok:
            error_string = "There was an error. Please try again."
            return render_template("lookup.html.j2", error=error_string, form = form)
        if not response.json():
            error_string = "There was an error, most likely because the Pokemon you entered does not exist. Please try again."
            return render_template("lookup.html.j2", error=error_string, form = form)
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
        return render_template("lookup.html.j2", pokemon_table = pokemon_dict, form = form)
    return render_template("lookup.html.j2", form = form)