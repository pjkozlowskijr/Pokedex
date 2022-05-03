from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route("/", methods = ['GET'])
def index():
    return render_template("index.html.j2")

@app.route("/lookup", methods = ['GET', 'POST'])
def lookup():
    if request.method == "POST":
        name = request.form.get("name")
        url = f"https://pokeapi.co/api/v2/pokemon/{name}"
        response = requests.get(url).json()
        if not response.ok:
            error_string = "There was an error. Please try again."
            return render_template("lookup.html.j2", error=error_string)
        if not response.json():
            error_string = "There was an error, most likely because the Pokemon you entered does not exist. Please try again."
            return render_template("lookup.html.j2", error=error_string)
        pokemon_dict = {
            "name": response["species"]["name"],
            "sprite": response["sprites"]["front_shiny"],
            "base_experience": response["base_experience"],
            "ability_name": response["abilities"][0]["ability"]["name"],
            "attack_base": response["stats"][1]["base_stat"],
            "hp_base": response["stats"][0]["base_stat"],
            "defense_base":response["stats"][2]["base_stat"],
        }