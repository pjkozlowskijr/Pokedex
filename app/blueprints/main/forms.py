from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

class PokeLookupForm(FlaskForm):
    poke_name = StringField("Pok\u00e9mon Name")
    search = SubmitField("Search")