from flask import Flask, request, jsonify
import uuid
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__)
app.config.from_pyfile('config.py', silent=True)


db = SQLAlchemy(app)
migrate = Migrate(app, db)


import my_proj.views
import my_proj.model

