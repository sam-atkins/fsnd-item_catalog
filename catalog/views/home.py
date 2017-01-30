"""
Manages main page views for index ie catalogue,
for books in one category and one book
Blueprint: homePage
"""

# [START Imports]
# Flask & others
from flask import Blueprint, render_template

# SQLAlchemy
# from sqlalchemy import create_engine, asc, desc
from sqlalchemy import asc, desc
# from sqlalchemy.orm import sessionmaker

# Db
from catalog.database import db_session, Category, Book
# [END Imports]


homePage = Blueprint('homePage', __name__)


# [START Database set-up]
# engine = create_engine(
#     'sqlite:////vagrant/fsnd-item_catalog/catalog/cataloguebooksv2.db')

# Base.metadata.bind = engine

# DBSession = sessionmaker(bind=engine)
# session = DBSession()
# [END Database set-up]


# [START Routes]
# Home /index
@homePage.route('/')
@homePage.route('/catalogue')
def index():
    categories = db_session.query(Category).order_by(asc(Category.name))
    books = db_session.query(Book).order_by(desc(Book.created_at))
    return render_template('index.html', categories=categories, books=books)
# [END Routes]
