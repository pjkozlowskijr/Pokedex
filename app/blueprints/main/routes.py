from flask import redirect, render_template, request, flash, url_for, g
import requests
from .forms import PokeLookupForm
from flask_login import login_required, current_user
from .import bp as main
from ...models import Pokemon, User, Battle

@main.route("/", methods=["GET"])
def index():
    return render_template("index.html.j2")

@main.route("/lookup", methods=["GET", "POST"])
@login_required
def lookup():
    form = PokeLookupForm()
    if request.method == "POST":
        pokemon = form.poke_name.data.lower()
        if not Pokemon.is_poke_in_db(pokemon):
            url_base = f"https://pokeapi.co/api/v2/pokemon/{pokemon}"
            response_base = requests.get(url_base)
            if not response_base.ok:
                flash("There was an error, most likely because the Pok\u00e9mon you entered does not exist. Please try again.", "danger")
                return render_template("lookup.html.j2", form=form)
            if not response_base.json():
                flash("There was an unexpected error. Please try again.", "danger")
                return render_template("lookup.html.j2", form=form)
            poke_data = response_base.json()
            inches = round(poke_data["height"] * 3.937)
            pokemon_dict = {
                "name": poke_data["species"]["name"],
                "poke_id_num": poke_data["id"],
                "height": f"{str(int(inches//12))}' {str(int(inches%12))}\"",
                "weight": f"{round(poke_data['weight']/4.536, 1)} lbs",
                "sprite": poke_data["sprites"]["other"]["home"]["front_default"],
                "base_experience": poke_data["base_experience"],
                "ability_name": poke_data["abilities"][0]["ability"]["name"],
                "attack_base": poke_data["stats"][1]["base_stat"],
                "hp_base": poke_data["stats"][0]["base_stat"],
                "defense_base":poke_data["stats"][2]["base_stat"],
            }
            female = requests.get("https://pokeapi.co/api/v2/gender/1/").json()
            male = requests.get("https://pokeapi.co/api/v2/gender/2/").json()
            female_list = [x["pokemon_species"]["name"] for x in female["pokemon_species_details"]]
            male_list = [y["pokemon_species"]["name"] for y in male["pokemon_species_details"]]
            if pokemon_dict["name"] in female_list:
                if pokemon_dict["name"] in male_list:
                    pokemon_dict["gender"] = "M\u2642 or F\u2640"
                else:
                    pokemon_dict["gender"] = "F\u2640"
            elif pokemon_dict["name"] in male_list:
                pokemon_dict["gender"] = "M\u2642"
            else:
                pokemon_dict["gender"] = "Unknown"
            for x in range(1, 10):
                habitat = requests.get(f"https://pokeapi.co/api/v2/pokemon-habitat/{x}/").json()
                habitat_list = [y["name"] for y in habitat["pokemon_species"]]
                if pokemon_dict["name"] in habitat_list:
                    pokemon_dict["habitat"] = habitat["name"]
            new_poke = Pokemon()
            new_poke.poke_to_db(pokemon_dict)
            new_poke.save_poke()
            return render_template("lookup.html.j2", pokemon_table=pokemon_dict, form=form)
        else:
            pokemon_dict = Pokemon.query.filter_by(name=pokemon).first()
            return render_template("lookup.html.j2", pokemon_table=pokemon_dict, form=form)
    return render_template("lookup.html.j2", form=form)

@main.route("/catch/<string:name>")
@login_required
def catch(name):
    poke = Pokemon().query.filter_by(name=name).first()
    if not current_user.check_user_has_poke(poke) and current_user.pokemon.count() < 5:
        current_user.catch_poke(poke)
        flash(f"{poke.name.title()} was added to your collection.", "success")
        return redirect(url_for("main.view_collection"))
    elif current_user.check_user_has_poke(poke):
        flash("You already have this Pok\u00e9mon in your collection.", "danger")
        return redirect(url_for("main.lookup"))
    elif current_user.pokemon.count() == 5:
        flash("You already have 5 Pok\u00e9mon in your collection. Please remove a Pok\u00e9mon before adding.", "danger")
        return redirect(url_for("main.view_collection"))
    flash("There was an unexpected error.")
    return redirect(url_for("main.lookup"))

@main.route("/release/<string:name>")
@login_required
def release(name):
    poke = Pokemon().query.filter_by(name=name).first()
    if current_user.check_user_has_poke(poke):
        current_user.release_poke(poke)
        flash(f"You released {poke.name.title()}.", "success")
        return redirect(request.referrer or url_for("main.view_collection"))
    flash("You cannot release a Pok\u00e9mon that is not in your collection.")
    return redirect(url_for("main.lookup"))

@main.route("/view_collection")
@login_required
def view_collection():
    if current_user.pokemon.count() > 0:
        return render_template("view_collection.html.j2", pokemon=current_user.pokemon, user=current_user)
    flash("You must add Pok\u00e9mon to view your collection.", "danger")
    return redirect(url_for("main.lookup"))

@main.route("/view_users")
@login_required
def view_users():
    users = User.query.filter(User.id != current_user.id, User.pokemon).all()
    return render_template("view_users.html.j2", users=users)

@main.route("/view_user_pokemon/<int:id>")
@login_required
def view_user_pokemon(id):
    user = User.query.get(id)
    if user.pokemon:
        return render_template("view_collection.html.j2", pokemon=user.pokemon, user=user)
    flash("This user has not caught any Pok\u00e9mon to view.")
    return redirect(url_for("main.view_users"))

@main.route("/start_battle/<int:id>")
@login_required
def start_battle(id):
    opponent = User.query.get(id)
    Battle.clear_squads()
    Battle.make_user_squad()
    Battle.make_opp_squad(opponent)
    return render_template("start_battle.html.j2", user_poke=Battle.user_squad, opp_poke=Battle.opp_squad, opponent=opponent)

@main.route("/launch_attack/<int:id>")
@login_required
def launch_attack(id):
    opponent = User.query.get(id)
    Battle.clear_results()
    Battle.attack_seq()
    if Battle.check_user_squad(id) and Battle.check_opp_squad(id):
        return render_template("continue_battle.html.j2", user_poke=Battle.user_squad, opp_poke=Battle.opp_squad, opponent=opponent, results=Battle.results)
    elif Battle.check_user_squad(id) == True or Battle.check_opp_squad(id) == True:
        return redirect(url_for("main.results"))

@main.route("/results")
@login_required
def results():
    return render_template("results.html.j2", results=Battle.results, winner=Battle.winner)
