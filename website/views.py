from flask import Blueprint, render_template, request, flash, jsonify
from .models import User
from flask_login import login_required, current_user
from .models import Note
from . import db 
import json
from sqlalchemy.sql.expression import func

views = Blueprint("views", __name__)

@views.route("/", methods = ["GET", "POST"])
@login_required
def home():
    if request.method == "POST":
        note = request.form.get("note")
        tags = request.form.get("tags")
        data_recipe = request.form.get("data_recipe")

        # Capitalize tags if not already capitalized
        tags = ', '.join(tag.strip().capitalize() for tag in tags.split(','))

        if len(note) < 1:
            flash("Note is too short!", category = "error")
        else:
            new_note = Note(data = note, user_id = current_user.id, tags=tags, data_recipe = data_recipe)
            db.session.add(new_note)
            db.session.commit()
            flash("Note added!", category = "success")
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
    return render_template('meal_picker.html', user=current_user, tags=tags)

@views.route("/recipies", methods = ["GET"])
@login_required
def recipies():
    return render_template('recipies.html', user=current_user)

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
                        'recipe': random_note.data_recipe})
    else:
        return jsonify({'note': 'No notes available'})

