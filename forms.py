from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SelectField, BooleanField
from wtforms.validators import InputRequired, Length, Email, URL, Optional


class RegisterForm(FlaskForm):
    """Registration form"""

    username = StringField(
        "Username", validators=[InputRequired(), Length(max=20)],
    )
    password = PasswordField(
        "Password", validators=[InputRequired()],
    )
    email = StringField(
        "Email", validators=[InputRequired(), Email(), Length(max=50)],
    )
    first_name = StringField(
        "First Name", validators=[InputRequired(), Length(max=30)],
    )
    last_name = StringField(
        "Last Name", validators=[InputRequired(), Length(max=30)],
    )

class LoginForm(FlaskForm):
    """Login form"""

    username = StringField(
        "Username", validators=[InputRequired(), Length(max=20)],
    )
    password = PasswordField(
        "Password", validators=[InputRequired()],
    )

class RecipeForm(FlaskForm):
    """Add user recipe form"""

    name = StringField(
        "Recipe Name", render_kw={"placeholder": "Enter your recipe name"},
        validators=[InputRequired()],
    )

    photo_url = StringField(
        "Photo URL", render_kw={"placeholder": "Optional"},
        validators=[Optional(), URL()],
    )

    ingredients = TextAreaField(
        "Ingredients (drag lower right corner to expand textbox)", render_kw={"placeholder": "Press enter for a new line"},
        validators=[InputRequired()],
    )

    instructions = TextAreaField(
        "Instructions (drag lower right corner to expand textbox)", render_kw={"placeholder": "Press enter for a new line"},
        validators=[InputRequired()],
    )

    favorite = BooleanField('Favorite?')
    

class DeleteForm(FlaskForm):
    """Delete form - used for validation"""

class FavForm(FlaskForm):
    """Favorites form - edit favorited recipes"""

    name = StringField(
        "Recipe Name", render_kw={"placeholder": "Enter your recipe name"},
        validators=[InputRequired()],
    )

    photo_url = StringField(
        "Photo URL", render_kw={"placeholder": "Optional"},
        validators=[Optional(), URL()],
    )

    ingredients = TextAreaField(
        "Ingredients (drag lower right corner to expand textbox)", render_kw={"placeholder": "Press enter for a new line"},
        validators=[InputRequired()],
    )

    instructions = TextAreaField(
        "Instructions (drag lower right corner to expand textbox)", render_kw={"placeholder": "Press enter for a new line"},
        validators=[InputRequired()],
    )


    




    