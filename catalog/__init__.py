from flask import Flask
# from flask_wtf.csrf import CSRFProtect
from .views.home import homePage
from .views.categories import category_admin
from .views.books import book_admin
from .views.json_api import api_admin
from .views.user_connect import user_admin


app = Flask(__name__)
app.register_blueprint(homePage)
app.register_blueprint(category_admin)
app.register_blueprint(book_admin)
app.register_blueprint(api_admin)
app.register_blueprint(user_admin)
# csrf = CSRFProtect()


# def create_app():
#     app = Flask(__name__)
#     csrf.init_app(app)
