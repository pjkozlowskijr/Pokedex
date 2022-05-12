from app import db, login
from flask_login import UserMixin, current_user
from datetime import datetime as dt
from werkzeug.security import generate_password_hash, check_password_hash
import re

user_poke = db.Table("user_poke",
    db.Column("poke_id", db.Integer, db.ForeignKey("pokemon.id")),
    db.Column("user_id", db.Integer, db.ForeignKey("user.id"))
)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    fav_pokemon = db.Column(db.String)
    email = db.Column(db.String, unique=True, index=True)
    password = db.Column(db.String)
    created_on = db.Column(db.DateTime, default=dt.utcnow)
    icon = db.Column(db.String)
    pokemon = db.relationship(
        "Pokemon",
        secondary=user_poke,
        backref="user_poke",
        lazy="dynamic",
        )
    battles = db.Column(db.Integer, default=0)
    wins = db.Column(db.Integer, default=0)
    losses = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f"<User: {self.email} | {self.id}"

    def __str__(self):
        return f"<User: {self.email} | {self.first_name} {self.last_name}"

    def hash_password(self, original_password):
        return generate_password_hash(original_password)

    def confirm_password(self, login_password):
        return check_password_hash(self.password, login_password)
    
    def form_to_db(self, data):
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.fav_pokemon = data["fav_pokemon"].title()
        self.email = data["email"]
        self.password = self.hash_password(data["password"])
        self.icon = data["icon"]

    def save(self):
        db.session.add(self)
        db.session.commit()

    def get_icon_url(self):
        search = re.search("^[0-9]", self.icon)
        if search:
            icon = int(self.icon)
            return f"https://avatars.dicebear.com/api/bottts/{icon}.svg"
        return self.icon

    def check_user_has_poke(self, poke_to_check):
        return poke_to_check in self.pokemon
    
    def catch_poke(self, poke_to_catch):
        self.pokemon.append(poke_to_catch)
        db.session.commit()

    def release_poke(self, poke_to_rel):
        self.pokemon.remove(poke_to_rel)
        db.session.commit()

    def show_pokemon(self):
        self_pokemon = self.pokemon
        collected = Pokemon.query.join(user_poke, (Pokemon.user_id == user_poke.c.user_id)).filter(user_poke.c.poke_id == self.id)
        user_pokemon = collected.union(self_pokemon).order_by(Pokemon.name)
        return user_pokemon

@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Pokemon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, index=True, unique=True)
    poke_id_num = db.Column(db.Integer)
    height = db.Column(db.String)
    weight = db.Column(db.String)
    sprite = db.Column(db.String)
    base_experience = db.Column(db.Integer)
    ability_name = db.Column(db.String)
    attack_base = db.Column(db.Integer)
    hp_base = db.Column(db.Integer)
    defense_base = db.Column(db.Integer)
    gender = db.Column(db.String)
    habitat = db.Column(db.String)

    def __repr__(self):
        return f"<Pokemon: {self.id} | {self.name}>"

    @classmethod
    def is_poke_in_db(cls, name):
        return Pokemon.query.filter_by(name=name).count()>0
        # return self.query.get(user_poke, (self.user_id == user_poke.c.user_id)).filter(user_poke.c.poke_id == self.id).first()

    def poke_to_db(self, poke_dict):
        self.name = poke_dict["name"]
        self.poke_id_num = poke_dict["poke_id_num"]
        self.height = poke_dict["height"]
        self.weight = poke_dict["weight"]
        self.sprite = poke_dict["sprite"]
        self.base_experience = poke_dict["base_experience"]
        self.ability_name = poke_dict["ability_name"]
        self.attack_base = poke_dict["attack_base"]
        self.hp_base = poke_dict["hp_base"]
        self.defense_base = poke_dict["defense_base"]
        self.gender = poke_dict["gender"]
        self.habitat = poke_dict["habitat"]

    def save_poke(self):
        db.session.add(self)
        db.session.commit()

class Battle:
    results = []
    user_squad = []
    opp_squad = []
    winner = []
    
    @classmethod
    def make_user_squad(cls):
        for poke in current_user.pokemon:
            poke_dict = {
                "owner": current_user.first_name,
                "name": poke.name,
                "sprite": poke.sprite,
                "hp": poke.hp_base,
                "attack": poke.attack_base,
                "defense": poke.defense_base,
            }
            Battle.user_squad.append(poke_dict)

    @classmethod
    def make_opp_squad(cls, opp):
        for poke in opp.pokemon:
            poke_dict = {
                "owner": opp.first_name,
                "name": poke.name,
                "sprite": poke.sprite,
                "hp": poke.hp_base,
                "attack": poke.attack_base,
                "defense": poke.defense_base,
            }
            Battle.opp_squad.append(poke_dict)

    @classmethod
    def attack_seq(cls):
        while Battle.opp_squad[0]["hp"] > 0 or Battle.user_squad[0]["hp"] > 0:
            if Battle.user_squad[0]["attack"] - Battle.opp_squad[0]["defense"] > 0:
                if Battle.opp_squad[0]["hp"] - (Battle.user_squad[0]["attack"] - Battle.opp_squad[0]["defense"]) <= 0:
                    Battle.opp_squad[0]["hp"] = 0
                else:
                    Battle.opp_squad[0]["hp"] -= Battle.user_squad[0]["attack"] - Battle.opp_squad[0]["defense"]
                Battle.results.append(f"{Battle.opp_squad[0]['name'].title()}'s HP was reduced to {Battle.opp_squad[0]['hp']} from the attack by {Battle.user_squad[0]['name']}.")
            else:
                Battle.opp_squad[0]["defense"] -= Battle.user_squad[0]["attack"]
                Battle.results.append(f"{Battle.opp_squad[0]['name'].title()}'s Defense was reduced to {Battle.opp_squad[0]['defense']} from the attack by {Battle.user_squad[0]['name']}.")
            if Battle.opp_squad[0]["hp"] == 0:
                elim_poke = Battle.opp_squad.pop(0)
                Battle.results.append(f"{elim_poke['name'].title()} has been eliminated.")
                break

            if Battle.opp_squad[0]["attack"] - Battle.user_squad[0]["defense"] > 0:
                if Battle.user_squad[0]["hp"] - (Battle.opp_squad[0]["attack"] - Battle.user_squad[0]["defense"]) <= 0:
                    Battle.user_squad[0]["hp"] = 0
                else:
                    Battle.user_squad[0]["hp"] -= Battle.opp_squad[0]["attack"] - Battle.user_squad[0]["defense"]
                Battle.results.append(f"{Battle.user_squad[0]['name'].title()}'s HP was reduced to {Battle.user_squad[0]['hp']} from the attack by {Battle.opp_squad[0]['name']}.")
            else:
                Battle.user_squad[0]["defense"] -= Battle.opp_squad[0]["attack"]
                Battle.results.append(f"{Battle.user_squad[0]['name'].title()}'s Defense was reduced to {Battle.user_squad[0]['defense']} from the attack by {Battle.opp_squad[0]['name']}.")
            if Battle.user_squad[0]["hp"] == 0:
                elim_poke = Battle.user_squad.pop(0)
                Battle.results.append(f"{elim_poke['name'].title()} has been eliminated.")
                break

    @classmethod
    def check_opp_squad(cls, id):
        opponent = User.query.get(id)
        if not Battle.opp_squad:
            Battle.results.append(f"{Battle.user_squad[0]['owner'].upper()} WINS!!!")
            current_user.wins += 1
            current_user.battles += 1
            current_user.save()
            Battle.winner.append(current_user)
            opponent.losses += 1
            opponent.battles += 1
            opponent.save()
            return False
        else:
            return True

    @classmethod
    def check_user_squad(cls, id):
        opponent = User.query.get(id)
        if not Battle.user_squad:
            Battle.results.append(f"{Battle.opp_squad[0]['owner'].upper()} WINS!!!")
            opponent.wins += 1
            opponent.battles += 1
            opponent.save()
            Battle.winner.append(opponent)
            current_user.losses += 1
            current_user.battles += 1
            current_user.save()
            return False
        else:
            return True

    @classmethod
    def clear_results(cls):
        Battle.results = []

    @classmethod
    def clear_squads(cls):
        Battle.user_squad = []
        Battle.opp_squad = []