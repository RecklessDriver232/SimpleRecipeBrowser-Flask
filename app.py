import os
import random
from flask import (
    Flask,
    flash,
    request,
    redirect,
    url_for,
    render_template,
    session,
    request,
)
from werkzeug.utils import secure_filename


from flask_wtf.csrf import CSRFProtect
from forms import AddNewRecipe, SignUp, SignIn, GoToNewRecipe
from databaseManagement import DB
import hashlib

app = Flask(__name__)
csrf = CSRFProtect(app)
app.secret_key = os.environ["APPSECRETKEY"]
PASSWORD_SALT = os.environ["PASSWORDSALT"]

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}
UPLOAD_FOLDER = r"C:\Users\risha\OneDrive\Documents\C_C++\Software_Engineering_project\static\Recipe_Pictures"


@app.before_request
def make_session_temp():
    if session.get("username", None) == None and request.endpoint not in [
        "signin",
        "signup",
        "static",
        "logout",
    ]:
        return redirect(url_for("signin"))
    if session.get("username", None) != None and request.endpoint in [
        "signin",
        "signup",
    ]:
        return redirect(url_for("home"))
    session.permanent = False


@app.errorhandler(404)
def not_found(e):
    return redirect(url_for("home"))


@app.route("/signup", methods=["POST", "GET"])
def signup():
    db = DB()
    form = SignUp()
    if form.validate_on_submit():
        username = request.form.get("Username")
        name = request.form.get("Name")
        email = request.form.get("Email")
        password = request.form.get("Password")
        confirm_password = request.form.get("Confirm_Password")
        if len(db.query(r"select * from User where Username = '%s'" % (username))) != 0:
            session["error"] = "Username Already Exists"
            return redirect(url_for("signup"))
        elif len(db.query(r"select * from User where Email = '%s'" % (email))) != 0:
            session["error"] = "Email Already Exists"
            return redirect(url_for("signup"))
        password += PASSWORD_SALT
        db.query(
            r"insert into User(Username, Name, Email, Password) values('%s','%s','%s','%s')"
            % (username, name, email, hashlib.md5(password.encode()).hexdigest())
        )
        session["message"] = "Successfully Signed Up"
        return redirect(url_for("signin"))
    else:
        username = request.form.get("Username")
        name = request.form.get("Name")
        email = request.form.get("Email")
        password = request.form.get("Password")
        confirm_password = request.form.get("Confirm_Password")
        if password != confirm_password:
            session["error"] = "Passwords do not match"
            return redirect(url_for("signup"))

    error = session.pop("error", None)
    message = session.pop("message", None)
    return render_template("index.html", error=error, message=message, form=form)


@app.route("/signin", methods=["POST", "GET"])
def signin():
    db = DB()
    form = SignIn()
    if form.validate_on_submit():
        username = request.form.get("UsernameorEmail")
        password = request.form.get("Password")
        password = password + PASSWORD_SALT
        password = hashlib.md5(password.encode()).hexdigest()
        if (
            len(
                db.query(
                    r"select * from User where Username = '%s' and Password = '%s'"
                    % (username, password)
                )
            )
            == 0
        ):
            if (
                len(
                    db.query(
                        r"select * from User where Email = '%s' and Password = '%s'"
                        % (username, password)
                    )
                )
                == 0
            ):
                session["error"] = "Email/Username does not match"
                return redirect(url_for("signin"))
            else:
                session["username"] = db.query(
                    r"select Username from User where Email = '%s'" % (username)
                )[0]["Username"]
                return redirect(url_for("home"))
        else:
            session["username"] = username
            return redirect(url_for("home"))

    error = session.pop("error", None)
    message = session.pop("message", None)
    return render_template("signin.html", error=error, message=message, form=form)


@app.route("/home", methods=["POST", "GET"])
def home():
    paths = {}
    db = DB()
    form = GoToNewRecipe()
    RecipeAll = db.query(r"select * from recipe;")
    for item in RecipeAll:
        if os.path.exists(os.path.join(UPLOAD_FOLDER, str(item["RecipeId"]) + ".jpg")):
            item["Image"] = os.path.join(str(item["RecipeId"]) + ".jpg")
        else:
            item["Image"] = os.path.join("Default_Picture.jpg")

    if form.validate_on_submit():
        recipeid = int(request.form.get("RecipeId"))
        return redirect(url_for("recipe", RecipeId=recipeid))
    return render_template("home.html", RecipeAll=RecipeAll, paths=paths, form=form)


@app.route("/home/<int:RecipeId>", methods=["POST", "GET"])
def recipe(RecipeId):
    db = DB()
    recipe = db.query(
        r"select Recipe,Description,CookingTime,DifficultyLevel,Username,Rating from Recipe where RecipeId = '%s'"
        % (RecipeId)
    )
    recipename = db.query(
        r"select RecipeName from Recipe where RecipeId = '%s'" % (RecipeId)
    )
    RecipeAll = db.query(r"select * from recipe;")
    if os.path.exists(os.path.join(UPLOAD_FOLDER, str(RecipeId) + ".jpg")):
        paths = os.path.join(str(RecipeId) + ".jpg")
    else:
        paths = os.path.join("Default_Picture.jpg")
    return render_template(
        "recipepage.html",
        recipename=recipename[0]["RecipeName"],
        recipe=recipe[0]["Recipe"],
        RecipeId=str(RecipeId),
        cookingtime=recipe[0]["CookingTime"],
        difficultylevel=recipe[0]["DifficultyLevel"],
        username=recipe[0]["Username"],
        rating=recipe[0]["Rating"],
        description=recipe[0]["Description"],
        paths=paths,
    )


@app.route("/addrecipe", methods=["POST", "GET"])
def addrecipe():
    form = AddNewRecipe()
    db = DB()
    if form.validate_on_submit():
        recipeid = random.randint(1000, 9999)
        existingid = [i["RecipeId"] for i in db.query(r"select RecipeId from Recipe;")]
        try:
            while recipeid in existingid:
                recipeid = random.randint(1000, 9999)
        except Exception as e:
            session["error"] = "Sorry my program aint the best"
        recipename = request.form.get("RecipeName")
        difficullty = request.form.get("DifficultyLevel")
        cookingtime = request.form.get("CookingTime")
        description = request.form.get("Description")
        recipe = request.form.get("Recipe")
        file = request.files["RecipePhoto"]
        if file:
            filename = str(recipeid) + ".jpg"
            file.save(os.path.join(UPLOAD_FOLDER, filename))
        db.query(
            r"insert into Recipe(RecipeId, Username, RecipeName, DifficultyLevel, CookingTime, Description, Recipe) values (%s, '%s','%s',%s ,%s ,'%s','%s')"
            % (
                recipeid,
                session["username"],
                recipename,
                difficullty,
                cookingtime,
                description,
                recipe,
            )
        )
        session["message"] = "Successful Added the Recipe"
        return redirect(url_for("addrecipe"))
    if form.errors:
        session["error"] = "Only JPG, JPEG, PNG are allowed"
        return redirect(url_for("addrecipe"))
    error = session.pop("error", None)
    message = session.pop("message", None)
    return render_template("addrecipe.html", error=error, message=message, form=form)


@app.route("/logout")
def logout():
    session.pop("username", None)
    session["message"] = "Successfully Logged Out"
    return redirect(url_for("signin"))


if __name__ == "__main__":
    context = (
        r"C:\Program Files\Git\usr\bin\server.crt",
        r"C:\Program Files\Git\usr\bin\server.key",
    )  # certificate and key files
    app.run(debug=True, ssl_context=context)
