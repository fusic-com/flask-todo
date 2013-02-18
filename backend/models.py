from flask.ext.sqlalchemy import SQLAlchemy

from .app import app

db = SQLAlchemy(app)
app.db = db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    active = db.Column(db.Boolean, nullable=False, default=True)

    def is_authenticated(self):
        return True
    def is_active(self):
        return self.active
    def is_anonymous(self):
        return False
    def get_id(self):
        return unicode(self.id)

    def __init__(self, username):
        self.username = username

    def __repr__(self):
        return '<User %r>' % self.username

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), unique=False)
    completed = db.Column(db.Boolean, nullable=False, default=False)
