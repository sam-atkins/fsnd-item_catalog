"""
Manages main page views for index ie catalogue,
for books in one category and one book
"""

# [START Imports]
# Flask & others
from flask import Blueprint, render_template

# SQLAlchemy
from sqlalchemy import create_engine, asc, desc
from sqlalchemy.orm import sessionmaker

# Db
from catalog.models import Base, Category, Book
# [END Imports]


home = Blueprint('home', __name__)


# [START Database set-up]
engine = create_engine(
    'sqlite:////vagrant/fsnd-item_catalog/catalog/cataloguebooksv2.db')

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()
# [END Database set-up]


# [START Routes]
# Home /index
@home.route('/')
@home.route('/catalogue')
def index():
    categories = session.query(Category).order_by(asc(Category.name))
    books = session.query(Book).order_by(desc(Book.created_at))
    return render_template('index.html', categories=categories, books=books)


# show books in one category
@home.route('/category/<int:category_id>/')
def showBooks(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    books = session.query(Book).filter_by(category_id=category_id).all()
    return render_template('categorybooks.html',
                           category_id=category_id, category=category,
                           books=books)


# display one book
@home.route('/book/<int:book_id>')
def theBook(book_id):
    book = session.query(Book).filter_by(id=book_id).one()
    return render_template('book.html', book=book)
# [END Routes]
