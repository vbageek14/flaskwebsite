from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from datetime import datetime, timezone

class Note(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    data = db.Column(db.String(10000))
    data_recipe = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone = True), default = datetime.now(timezone.utc))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    tags = db.Column(db.String(250))

    @property
    def tag_names(self)->list:
        return [tag.strip() for tag in self.tags.split(',') if tag.strip()]

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(150), unique = True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    notes = db.relationship("Note")
    



