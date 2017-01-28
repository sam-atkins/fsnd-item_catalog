from flask import Flask
from flask_wtf.csrf import CSRFProtect
from .views.home import home
from .views.category import category
from .views.books import books
from .views.json_api import json_api
from .views.signin import signin


app = Flask(__name__)
app.register_blueprint(home)
app.register_blueprint(category)
app.register_blueprint(books)
app.register_blueprint(json_api)
app.register_blueprint(signin)
csrf = CSRFProtect()


def create_app():
    app = Flask(__name__)
    csrf.init_app(app)
