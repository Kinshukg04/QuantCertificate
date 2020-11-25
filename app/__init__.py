from flask import Flask, render_template, session
from flask_sqlalchemy import SQLAlchemy
import os

# Configurations
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')
app.config['UPLOAD_FOLDER'] = os.environ.get('UPLOAD_FOLDER')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS')
app.config['MAX_CONTENT_LENGTH'] = int(os.environ.get('MAX_CONTENT_LENGTH'))
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

# Create database
db = SQLAlchemy(app)

from app.models import models
db.create_all()

from app.views import views

