#!/usr/bin/env python3
from models import db
from flask_migrate import Migrate
from flask import Flask
from flask_restful import Api
from routes import app as api_bp
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False
app.register_blueprint(api_bp)

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)


@app.route("/")
def index():
    return "<h1>Code challenge</h1>"


if __name__ == "__main__":
    app.run(port=5555, debug=True)
