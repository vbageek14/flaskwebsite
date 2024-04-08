from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from datetime import datetime, timezone
from itsdangerous import URLSafeTimedSerializer as Serializer
from website import app, config

SECRET_KEY = config.SECRET_KEY.encode("utf-8")

class Note(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    data = db.Column(db.String(10000))
    data_recipe = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone = True), default = datetime.now(timezone.utc))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    tags = db.Column(db.String(250))
    recipe_link = db.Column(db.String(1000))

    @property
    def tag_names(self)->list:
        return [tag.strip().title() for tag in self.tags.split(',') if tag.strip()]

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(150), unique = True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    notes = db.relationship("Note")

    def get_reset_token(self):
        s = Serializer(SECRET_KEY)
        return s.dumps({"user_id": self.id})
    
    @staticmethod
    def verify_reset_token(token, expiration = 1800):
        s = Serializer(SECRET_KEY)
        try:
            id = s.loads(token, expiration)["user_id"]
        except:
            return None
        return User.query.get(id)

    



