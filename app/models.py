from app import db, login
from flask_login import UserMixin
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
        backref=db.backref("user", lazy="dynamic"), 
        lazy="dynamic"
        )

    def __repr__(self):
        return f"<User: {self.email} | {self.user_id}"

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
        return self.pokemon.filter(user_poke.c.poke_id == poke_to_check).count()
    
    def add_poke(self, poke_to_add):
        if not self.check_user_has_poke(poke_to_add):
            self.pokemon.append(poke_to_add)
            db.session.commit()

    def del_poke(self, poke_to_del):
        if self.check_user_has_poke(poke_to_del):
            self.pokemon.remove(poke_to_del)
            db.session.commit()

    def show_pokemon(self):
        self_pokemon = self.pokemon
        collected = Pokemon.query.join(user_poke, (Pokemon.user_id == user_poke.c.user_id)).filter(user_poke.c.poke_id == self.id)
        user_pokemon = collected.union(self_pokemon)
        return user_pokemon

@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Pokemon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    poke_id_num = db.Column(db.Integer)
    # in total inches (convert later)
    height = db.Column(db.String)
    # in pounds
    weight = db.Column(db.String)
    sprite = db.Column(db.String)
    base_exp = db.Column(db.Integer)
    ability = db.Column(db.String)
    attack_base = db.Column(db.Integer)
    hp_base = db.Column(db.Integer)
    defense_base = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def __repr__(self):
        return f"<Pokemon: {self.id} | {self.name}>"

    def check_poke_collected(self):
        return user_poke.filter(user_poke.poke_id == self.id).first()

    def poke_to_db(self, poke_dict):
            self.name = poke_dict["name"].title()
            self.poke_id_num = poke_dict["id"]
            self.height = poke_dict["height"]
            self.weight = poke_dict["weight"]
            self.sprite = poke_dict["sprite"]
            self.base_exp = poke_dict["base_experience"]
            self.ability = poke_dict["ability_name"].title()
            self.attack_base = poke_dict["attack_base"]
            self.hp_base = poke_dict["hp_base"]
            self.defense_base = poke_dict["defense_base"]

    def save_poke(self):
        db.session.add(self)
        db.session.commit()