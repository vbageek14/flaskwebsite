from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from .models import User
from flask_login import login_required, current_user
from .models import Note
from . import db 
import json
from sqlalchemy.sql.expression import func
from .webforms import SearchForm


views = Blueprint("views", __name__)

@views.route("/", methods = ["GET", "POST"])
@login_required
def home():
    if request.method == "POST":
        note = request.form.get("note")
        tags = request.form.get("tags")
        data_recipe = request.form.get("data_recipe")
        recipe_link = request.form.get("recipe_link")

        # Capitalize tags if not already capitalized
        tags = ', '.join(tag.strip().capitalize() for tag in tags.split(','))

        if len(note) < 1:
            flash("Note is too short!", category = "error")
        else:
            new_note = Note(data = note, user_id = current_user.id, tags=tags, data_recipe = data_recipe, recipe_link = recipe_link)
            db.session.add(new_note)
            db.session.commit()
            flash("Note added!", category = "success")
            return redirect(url_for("views.recipies"))
    return render_template("home.html", user = current_user)

@views.route("/delete-note", methods = ["POST"])
def delete_note():
    note = json.loads(request.data)
    noteId = note["noteId"]
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
            return jsonify({})
    else:
        return jsonify({"message": "Deletion canceled"})
        
@views.route("/meal-picker", methods = ["GET"])
@login_required
def meal_picker():
    tags = set()
    notes = Note.query.all()
    for note in notes:
        tags.update(note.tag_names)
    tags = sorted(tags)
    return render_template('meal_picker.html', user=current_user, tags=tags)

@views.route("/recipies", methods = ["GET"])
@login_required
def recipies():
    tags = set()
    notes = Note.query.order_by(Note.data).all()

    return render_template('recipies.html', notes = notes, user=current_user)

@views.route("/random-note")
@login_required
def random_note():
    selected_tag = request.args.get('tag')
    if selected_tag:
        random_note = Note.query.filter(Note.tags.contains(selected_tag)).order_by(func.random()).first()
    else:
        random_note = Note.query.order_by(func.random()).first()

    if random_note:
        return jsonify({'note': random_note.data,
                        'recipe': random_note.data_recipe,
                        'link': random_note.recipe_link})
    else:
        return jsonify({'note': 'No recipies available'})
    
@views.route('/search', methods = ["POST"])
@login_required
def search():
    form = SearchForm()
    posts = Note.query
    if form.validate_on_submit():
        searched = form.searched.data 
        posts = posts.filter(Note.data_recipe.like("%" + searched + "%"))
        posts = posts.order_by(Note.data).all()
    else:
        print(form.errors)  # Print validation errors
    return render_template("search.html", form = form, searched = searched, posts = posts, user = current_user)

@views.route("/about", methods = ["GET"])
@login_required
def about():
    return render_template("about.html", user = current_user)