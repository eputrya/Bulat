from flask_login import UserMixin
from werkzeug.security import check_password_hash

from app import db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_active(self):
        return True

    def __repr__(self):
        return f"<User(id={self.id}, username={self.username})>"
