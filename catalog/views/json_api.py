"""
API JSON endpoints
"""

# [START Imports]
from flask import Blueprint, jsonify

# SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Db
from catalog.models import Base, Category, Book
# [END Imports]


json_api = Blueprint('json_api', __name__)


# [START Database set-up]
engine = create_engine(
    'sqlite:////vagrant/fsnd-item_catalog/catalog/cataloguebooksv2.db')

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()
# [END Database set-up]


# [START JSON API Endpoints]
@json_api.route('/categories/JSON')
def allCategoriesJSON():
    categories = session.query(Category).all()
    return jsonify(categories=[c.serialize for c in categories])


@json_api.route('/book/<int:book_id>/JSON')
def bookJSON(book_id):
    book = session.query(Book).filter_by(id=book_id).one()
    return jsonify(book=book.serialize)


@json_api.route('/category/<int:category_id>/JSON')
def categoryWithBooksJSON(category_id):
    books = session.query(Book).filter_by(id=category_id).all()
    return jsonify(Category=[b.serialize for b in books])
# [END JSON API Endpoints]
