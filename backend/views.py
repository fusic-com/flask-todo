from .app import app
from flask import render_template

@app.route('/')
def todo():
    return render_template("todo.html")
