from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class PokeLookupForm(FlaskForm):
    poke_name = StringField("Pok\u00e9mon Name", validators=[DataRequired()])
    search = SubmitField("Search")