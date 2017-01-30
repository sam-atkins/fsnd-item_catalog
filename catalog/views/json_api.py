"""
API JSON endpoints
"""

# [START Imports]
from flask import Blueprint, jsonify

# SQLAlchemy
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker

# Db
from catalog.database import db_session, Category, Book
# [END Imports]


api_admin = Blueprint('api_admin', __name__)


# [START Database set-up]
# engine = create_engine(
#     'sqlite:////vagrant/fsnd-item_catalog/catalog/cataloguebooksv2.db')

# Base.metadata.bind = engine

# DBSession = sessionmaker(bind=engine)
# session = DBSession()
# [END Database set-up]


# [START JSON API Endpoints]
@api_admin.route('/categories/JSON')
def allCategoriesJSON():
    categories = db_session.query(Category).all()
    return jsonify(categories=[c.serialize for c in categories])


@api_admin.route('/book/<int:book_id>/JSON')
def bookJSON(book_id):
    book = db_session.query(Book).filter_by(id=book_id).one()
    return jsonify(book=book.serialize)


@api_admin.route('/category/<int:category_id>/JSON')
def categoryWithBooksJSON(category_id):
    books = db_session.query(Book).filter_by(id=category_id).all()
    return jsonify(Category=[b.serialize for b in books])
# [END JSON API Endpoints]
