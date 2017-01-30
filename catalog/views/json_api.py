"""
API JSON endpoints
"""

# [START Imports]
from flask import Blueprint, jsonify

# Db
from catalog.database import db_session, Category, Book
# [END Imports]


api_admin = Blueprint('api_admin', __name__)


# [START JSON API Endpoints]
@api_admin.route('/categories/JSON')
def allCategoriesJSON():
    """
    Generates JSON for all categories
    """
    categories = db_session.query(Category).all()
    return jsonify(categories=[c.serialize for c in categories])


@api_admin.route('/book/<int:book_id>/JSON')
def bookJSON(book_id):
    """
    Generates JSON for a book specified by the book_id
    """
    book = db_session.query(Book).filter_by(id=book_id).one()
    return jsonify(book=book.serialize)


@api_admin.route('/category/<int:category_id>/JSON')
def categoryWithBooksJSON(category_id):
    """
    Generates JSON for a category with all books in the category
    Specified by the category_id
    """
    books = db_session.query(Book).filter_by(id=category_id).all()
    return jsonify(Category=[b.serialize for b in books])
# [END JSON API Endpoints]
