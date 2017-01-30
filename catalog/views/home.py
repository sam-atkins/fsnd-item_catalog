"""
Manages main page views for index ie catalogue,
for books in one category and one book
Blueprint: homePage
"""

# [START Imports]
# Flask & others
from flask import Blueprint, render_template

# SQLAlchemy
from sqlalchemy import asc, desc

# Db
from catalog.database import db_session, Category, Book
# [END Imports]


homePage = Blueprint('homePage', __name__)


# [START Routes]
# Home /index
@homePage.route('/')
@homePage.route('/catalogue')
def index():
    """Displays the index i.e. home page, with db queries made to return
    all categories in ascending order i.e. alphabetical order
    all books in descending order by created date
    """
    categories = db_session.query(Category).order_by(asc(Category.name))
    books = db_session.query(Book).order_by(desc(Book.created_at))
    return render_template('index.html', categories=categories, books=books)
# [END Routes]
