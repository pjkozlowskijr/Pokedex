from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, RadioField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from ...models import User
import random
from jinja2.utils import markupsafe

class RegisterForm(FlaskForm):
    first_name = StringField("First Name", validators=[DataRequired()])
    last_name = StringField("Last Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email(message="Invalid email format.")])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password", message="Passwords must match.")])
    submit = SubmitField("Register")

    av1 = random.randint(1, 1000)
    av2 = random.randint(1001, 2000)
    av3 = random.randint(2001, 3000)
    av4 = random.randint(3001, 4000)

    av1_img = markupsafe.Markup(f"<img src='https://avatars.dicebear.com/api/bottts/{av1}.svg' height='100px'")
    av2_img = markupsafe.Markup(f"<img src='https://avatars.dicebear.com/api/bottts/{av2}.svg' height='100px'")
    av3_img = markupsafe.Markup(f"<img src='https://avatars.dicebear.com/api/bottts/{av3}.svg' height='100px'")
    av4_img = markupsafe.Markup(f"<img src='https://avatars.dicebear.com/api/bottts/{av4}.svg' height='100px'")

    icon = RadioField("Select Avatar:", validators=[DataRequired()], choices = [(av1, av1_img), (av2, av2_img), (av3, av3_img), (av4, av4_img)])

    def validate_email(form, field):
        email_already_used = User.query.filter_by(email=field.data).first()
        if email_already_used:
            raise ValidationError("Email is already in use.")

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")

class EditProfileForm(FlaskForm):
    first_name = StringField("First Name", validators=[DataRequired()])
    last_name = StringField("Last Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password", message="Passwords must match.")])
    submit = SubmitField("Register")

    av1 = random.randint(1, 1000)
    av2 = random.randint(1001, 2000)
    av3 = random.randint(2001, 3000)
    av4 = random.randint(3001, 4000)

    av1_img = markupsafe.Markup(f"<img src='https://avatars.dicebear.com/api/bottts/{av1}.svg' height='100px'")
    av2_img = markupsafe.Markup(f"<img src='https://avatars.dicebear.com/api/bottts/{av2}.svg' height='100px'")
    av3_img = markupsafe.Markup(f"<img src='https://avatars.dicebear.com/api/bottts/{av3}.svg' height='100px'")
    av4_img = markupsafe.Markup(f"<img src='https://avatars.dicebear.com/api/bottts/{av4}.svg' height='100px'")

    icon = RadioField("Select Avatar:", validators=[DataRequired()], choices = [(9000, "Keep Avatar"), (av1, av1_img), (av2, av2_img), (av3, av3_img), (av4, av4_img)])