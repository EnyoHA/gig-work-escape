from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchmey()

app = Flask()

def login():
    if request.method == 'POST':
        email =
