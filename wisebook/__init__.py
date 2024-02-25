from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from wisebook.settings import Config


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from wisebook import views
