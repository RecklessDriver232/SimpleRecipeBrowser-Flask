from tarfile import LENGTH_NAME
from tokenize import String
from click import File
from flask_wtf import FlaskForm
from sqlalchemy import Integer
from wtforms import (
    EmailField,
    StringField,
    IntegerField,
    PasswordField,
    SubmitField,
    SelectField,
    DateField,
    TextAreaField,
    validators,
    FileField,
    HiddenField,
    EmailField,
)
from wtforms.validators import InputRequired, Length, EqualTo, NumberRange
from flask_wtf.file import FileAllowed


class SignUp(FlaskForm):
    Username = StringField("Username", validators=[InputRequired(), Length(max=16)])
    Name = StringField("Name", validators=[InputRequired(), Length(max=50)])
    Email = EmailField("Email", validators=[InputRequired(), Length(max=50)])
    Password = PasswordField(
        "Password",
        validators=[
            EqualTo("Confirm_Password", message="Passwords must match"),
            Length(min=8, max=20),
        ],
    )
    Confirm_Password = PasswordField(
        "Comfirm Password", validators=[InputRequired(), Length(min=8, max=20)]
    )
    Submit = SubmitField(label=("Submit"))


class SignIn(FlaskForm):
    UsernameorEmail = StringField(
        "Username", validators=[InputRequired(), Length(max=16)]
    )
    Password = PasswordField(
        "Password",
        validators=[
            Length(min=8, max=20),
        ],
    )
    Submit = SubmitField(label=("Submit"))


class AddNewRecipe(FlaskForm):
    RecipeName = StringField("Recipe Name", validators=[InputRequired()])
    DifficultyLevel = IntegerField(
        "Difficulty Level", validators=[InputRequired(), NumberRange(min=1, max=10)]
    )
    CookingTime = IntegerField("Cooking Time", validators=[InputRequired()])
    Description = StringField(
        "Description", validators=[InputRequired(), Length(max=50)]
    )
    Recipe = TextAreaField("Recipe", validators=[InputRequired()])
    RecipePhoto = FileField(
        "image", validators=[FileAllowed(["jpg", "jpeg", "png"], "Images Only")]
    )
    Submit = SubmitField(label="Submit")


class GoToNewRecipe(FlaskForm):
    RecipeId = HiddenField()
    Submit = SubmitField(label="Learn More")
