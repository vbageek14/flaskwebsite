from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from .models import User, RecipeNote
from flask_login import login_required, current_user
from . import db 
import json
from sqlalchemy.sql.expression import func
from .webforms import SearchForm, UpdateTagsForm

views = Blueprint("views", __name__)

# Define route for the home page where user inputs the recipe
@views.route("/", methods = ["GET", "POST"])
@login_required
def home():
    if request.method == "POST":
        recipe_name = request.form.get("recipe_name")
        tags = request.form.get("tags")
        recipe = request.form.get("recipe")
        recipe_link = request.form.get("recipe_link")

        # Capitalize tags if not already capitalized
        tags = ', '.join(tag.strip().capitalize() for tag in tags.split(','))

        if len(recipe_name) < 1:
            flash("Recipe name is too short!", category = "error")
        elif len(recipe) <1:
            flash("Recipe is too short!", category = "error")
        else:
            new_recipe_note = RecipeNote(recipe_name = recipe_name, user_id = current_user.id, tags=tags, recipe = recipe, recipe_link = recipe_link)
            db.session.add(new_recipe_note)
            db.session.commit()
            flash("Recipe added!", category = "success")
            return redirect(url_for("views.recipes"))
    return render_template("home.html", user = current_user)

# Define route for the delete-note functionality whereby user is able to delete a note from the "/Recipes" page
@views.route("/delete-recipe", methods = ["POST"])
def delete_recipe():
    note = json.loads(request.data)
    noteId = note["noteId"]
    note = RecipeNote.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
            return jsonify({})
    else:
        return jsonify({"message": "Deletion canceled"})
    
# Defines route for the meal picker functionality. Extracts tags from all recipes and displays them in a dropdown on the "/meal-picker" page   
@views.route("/meal-picker", methods = ["GET"])
@login_required
def meal_picker():
    tags = set()
    notes = RecipeNote.query.filter_by(user_id=current_user.id).all()
    for note in notes:
        tags.update(note.tag_names)
    tags = sorted(tags)
    return render_template('meal_picker.html', user=current_user, tags=tags)

# Defines route for recipes page where all input recipes are displayed
@views.route("/recipes", methods = ["GET"])
@login_required
def recipes():
    notes = RecipeNote.query.filter_by(user_id=current_user.id).order_by(RecipeNote.recipe_name).all()
    return render_template('recipes.html', notes = notes, user=current_user)

# Defines route for generating a random recipe based on a tag selected in the dropdown of the "/meal-picker" page
@views.route("/random-recipe")
@login_required
def random_recipe():
    selected_tag = request.args.get('tag')
    if selected_tag:   
        random_recipe = RecipeNote.query.filter(RecipeNote.user_id == current_user.id, RecipeNote.tags.contains(selected_tag)).order_by(func.random()).first()
    else:
        random_recipe = RecipeNote.query.filter_by(user_id=current_user.id).order_by(func.random()).first()

    if random_recipe:
        # return a JSON response used in the "mealPicker.js" function
        return jsonify({'note': random_recipe.recipe_name,
                        'recipe': random_recipe.recipe,
                        'link': random_recipe.recipe_link})
    else:
        return jsonify({'note': 'No recipes available'})
    
# Defines route for the search bar functionality
@views.route('/search', methods = ["POST"])
@login_required
def search():
    form = SearchForm()
    posts = RecipeNote.query
    if form.validate_on_submit():
        searched = form.searched.data 
        
        # perform a search across all user's recipes and the associated tags using the "searched" variable (user's input in the SearchForm)
        posts = posts.filter(RecipeNote.user_id == current_user.id, 
                             db.or_(RecipeNote.recipe.like("%" + searched + "%"),
                                    RecipeNote.tags.like("%" + searched + "%")))
        posts = posts.order_by(RecipeNote.recipe_name).all()
    else:
        print(form.errors) 
    return render_template("search.html", form = form, searched = searched, posts = posts, user = current_user)

# Defines route for the "about" page
@views.route("/about", methods = ["GET"])
@login_required
def about():
    return render_template("about.html", user = current_user)

# Defines route for the update_tags functionality which allows to update tags associated with particular recipe displayed on the "/recipes" page
@views.route("/update_tags/<int:id>", methods = ["GET", "POST"])
@login_required
def update_tags(id):
    form = UpdateTagsForm()
    note = RecipeNote.query.get(id)
    
    if form.validate_on_submit():
        if note.user_id == current_user.id:
            tags = request.form.get("tags")

             # Capitalize tags if not already capitalized
            tags = ', '.join(tag.strip().capitalize() for tag in tags.split(','))

            note.tags = tags

            db.session.commit()
            flash("Tags updated successfully", category="success")
            return redirect(url_for("views.recipes"))
        else:
            return jsonify({"message": "Deletion canceled"})

    form.tags.data = note.tags  
    return render_template("update_tags.html", form=form, note=note, user=current_user)


# Defines route for the "disclaimer" page
@views.route("/disclaimer", methods = ["GET"])
def disclaimer():
    return render_template("disclaimer.html", user = current_user)