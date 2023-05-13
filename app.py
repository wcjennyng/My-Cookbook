from flask import Flask, request, redirect, render_template, session, jsonify, flash, abort
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Recipes, Favorites
from forms import RegisterForm, LoginForm, RecipeForm, DeleteForm, FavForm
from sqlalchemy.exc import IntegrityError
import requests, random, datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///recipes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'secret_key'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False 

debug = DebugToolbarExtension(app)

connect_db(app)

@app.errorhandler(404)
def not_found(e):
    return redirect('/login')

@app.route('/')
def home_page():
    """Homepage. Redirects to login page"""
    return redirect ('/login')
    
#LOGIN/OUT AND REGISTER

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Register page"""

    if 'username' in session:
        return redirect(f"/users/{session['username']}")

    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        new_user = User.register(username, password, email, first_name, last_name)

        db.session.add(new_user)
        
       
        try:
            db.session.commit()
            session['username'] = new_user.username
            session['email'] = new_user.email
                
        except IntegrityError as e:
            errorMessage = e.orig.diag.message_detail
            if 'username' in errorMessage:
                form.username.errors.append('Username taken. Please choose another username.')
            if 'email' in errorMessage:
                form.email.errors.append('Email taken. Please choose another email.')   
            return render_template('register.html', form=form)
        
        return redirect(f"/users/{new_user.username}")
    else:
        return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login_user():
    """Login form"""

    if 'username' in session:
        return redirect(f"/users/{session['username']}")

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)

        if user:
            session['username'] = user.username
            return redirect(f"/users/{user.username}")
        else:
            form.username.errors = ["Invalid username/password."]

    return render_template('login.html', form=form)

@app.route('/logout')
def logout_user():
    session.pop('username')
    return redirect('/login')

@app.route('/users/<username>')
def user_page(username):
    """Page when user is logged in"""

    user = User.query.get(username)
    recipe = Recipes.query.all()
    form = LoginForm()

    if 'username' not in session or username != session['username']:
        form.username.errors = ["You are not authorized here."]
        return redirect ('/login')
    

    return render_template('user.html', user=user, form=form,recipe=recipe)

#RANDOM GENERATOR

@app.route('/users/<username>/random-recipe')
def random_page(username):
    """Shows main page of random generator"""

    form = LoginForm()

    if 'username' not in session or username != session['username']:
        form.username.errors = ["You are not authorized here."]
        return redirect ('/login')

    user = User.query.get(username)

    return render_template('randomrecipe.html', user=user, form=form)

@app.route('/api/randomrecipe', methods=['POST'])
def random_recipe():
    """Creates random recipe when letter is searched"""

    letter = request.json['letter']
    if letter == "": 
        return jsonify(random_err="Letter is required"), 500
    elif letter.lower() not in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 
                        'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']:
        return jsonify(random_err="Please enter a valid letter from the alphabet"), 500

    recipe = jsonify(letter=letter)

    if recipe:

        recipe_res = requests.get(f"https://www.themealdb.com/api/json/v1/1/search.php?f={letter}")
        recipe_obj = recipe_res.json()
        recipe_arr = recipe_obj['meals']
        return jsonify(recipe_arr=recipe_arr)

        

    return (recipe, 201)


#SEARCH RECIPE BY NAME/INGREDIENT

@app.route('/users/<username>/searchrecipe')
def search_recipepage(username):
    """Shows main page of searching a recipe"""

    form = LoginForm()

    if 'username' not in session or username != session['username']:
        form.username.errors = ["You are not authorized here."]
        return redirect ('/login')

    user = User.query.get(username)

    return render_template('searchrecipe.html', user=user, form=form)

@app.route('/api/searchrecipe', methods=['POST'])
def search_recipe():
    """Creates recipe when name/ingredient of recipe is searched"""

    name = request.json['name']
    if name == "":
        return jsonify(name_err="Name is required"), 500
    elif name.isalpha() == False:
        return jsonify(name_err="Not found. Please enter a valid name"), 500

    search = jsonify(name=name)

    if search:
        name_res = requests.get(f"https://www.themealdb.com/api/json/v1/1/search.php?s={name}")
        name_obj = name_res.json()
        meals_arr = name_obj['meals']
        return jsonify(meals_arr=meals_arr)
    return(search, 201)



#ADD USER RECIPE

@app.route('/users/<username>/userrecipe/add', methods=['GET', 'POST'])
def add_recipe(username):
    """New user recipe form. Adds new recipe to User Recipe Tab."""

    recipe = Recipes.query.all()
    user = User.query.all()

    if 'username' not in session or username != session['username']:
        form.username.errors = ["You are not authorized here."]
        return redirect ('/login')

    form = RecipeForm()

    if form.validate_on_submit():

        recipe = Recipes(
            name=form.name.data,
            photo_url=form.photo_url.data,
            ingredients=form.ingredients.data,
            instructions=form.instructions.data,
            favorite=form.favorite.data,
            username=username,
        )

        db.session.add(recipe)
        db.session.commit()

        return redirect(f"/users/{recipe.username}")

    else:

        return render_template('user_recipe/new.html', form=form, recipe=recipe, user=user)

@app.route('/userrecipe/<int:recipe_id>/update', methods=["GET", "POST"])
def update(recipe_id):
    """Edit form for user recipe. Updates user recipe"""

    recipe = Recipes.query.get(recipe_id)
    user = User.query.all()

    if 'username' not in session or recipe.username != session['username']:
        form.username.errors = ["You are not authorized here."]
        return redirect ('/login')

    form = RecipeForm(obj=recipe)

    if form.validate_on_submit():
        recipe.name = form.name.data
        recipe.photo_url=form.photo_url.data,
        recipe.ingredients=form.ingredients.data,
        recipe.instructions=form.instructions.data,
        recipe.favorite=form.favorite.data

        db.session.commit()

        return redirect(f"/users/{recipe.username}")

    return render_template('user_recipe/edit.html', form=form, recipe=recipe, user=user)

@app.route('/userrecipe/<int:recipe_id>/delete', methods=['POST'])
def delete_recipe(recipe_id):
    """Deletes user recipe"""

    recipe = Recipes.query.get(recipe_id)

    if "username" not in session or recipe.username != session['username']:
        form.username.errors = ["You are not authorized here."]
        return redirect ('/login')

    form = DeleteForm()

    if form.validate_on_submit():

        db.session.delete(recipe)
        db.session.commit()

    return redirect(f"/users/{recipe.username}")

#FAVORITES

@app.route('/users/<username>/favorites', methods=['GET', 'POST'])
def add_favorites(username):
    
    if 'username' not in session or username != session['username']:
        return redirect ('/login')


    form = DeleteForm()
    user = User.query.get(username)
    username = session['username']
    favorite = Favorites.query.all()
    
    recipe = Recipes.query.all()

    if request.method == 'POST':
        fav = request.json['fav']
        #creates an array for ingredients and measures
        ingredients = []
        measures =[]
        
        for m in range(1,21):
            measure = fav['strMeasure' + str(m)] + ' '
            if measure != '':
                measures.append(measure)
            else:
                break

        for i in range(1,21):
            ing = fav['strIngredient' + str(i)]
            if ing != '': 
                ingredients.append(ing)          
            else:
                break
        
        ingList = [x  + y for x,y in zip(measures, ingredients)]
        finalList = '\n '.join([eachIng for eachIng in ingList])


        favorite = Favorites(
            name=fav['strMeal'],
            photo_url=fav['strMealThumb'],
            ingredients=finalList,
            instructions=fav['strInstructions'],
            username=username,
        )


        db.session.add(favorite)
        db.session.commit()
        
        return render_template('favorites.html', user=user, username=username, favorite=favorite, recipe=recipe, form=form)
    else:
        """Shows favorites list"""


        if 'username' not in session:
            return redirect ('/login')
            
        
        user = User.query.get(username)
        username = session['username']
        form = DeleteForm()
        favorites = Favorites.query.filter_by(username=username).all()
        recipe = Recipes.query.all()

        return render_template('favorites.html', user=user, username=username, favorites=favorites, recipe=recipe, form=form)

@app.route('/users/<int:favorites_id>/update', methods=['GET', 'POST'])
def updateFav(favorites_id):
    """Edit form for favorited recipe. Updates favorited recipe"""

    favorite = Favorites.query.get(favorites_id)
    
    user = User.query.all()

    if 'username' not in session or favorite.username != session['username']:
        form.username.errors = ["You are not authorized here."]
        return redirect ('/login')


    form = FavForm(obj=favorite)

    if form.validate_on_submit():
        favorite.name = form.name.data
        favorite.photo_url=form.photo_url.data,
        favorite.ingredients=form.ingredients.data,
        favorite.instructions=form.instructions.data

        db.session.commit()

        return redirect(f"/users/{favorite.username}/favorites")
    
    return render_template('fav_recipe/edit.html', form=form, favorite=favorite, user=user)

@app.route('/users/<int:favorites_id>/delete', methods=['POST'])
def deleteFav(favorites_id):
    """Deletes favorited recipe"""

    favorite = Favorites.query.get(favorites_id)

    if "username" not in session or favorite.username != session['username']:
        form.username.errors = ["You are not authorized here."]
        return redirect ('/login')

    form = DeleteForm()

    if form.validate_on_submit():

        db.session.delete(favorite)
        db.session.commit()

    return redirect(f"/users/{favorite.username}/favorites")



    
