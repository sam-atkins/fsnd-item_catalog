"""
Application docstrings here
"""

# [START Imports]
# Flask
from flask import Flask, render_template

# SQLAlchemy
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker

# Db
from database_setup import Base, Category, Book
# [END Imports]


# [START Database set-up]
engine = create_engine('sqlite:///cataloguebooks.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()
# [END Database set-up]


# Flask
app = Flask(__name__)


# [START Routes]
# Home /index
@app.route('/')
@app.route('/catalogue')
@app.route('/category')
def index():
    # categories = session.query(Category).order_by(asc(Category.name))
    return render_template('index.html')


# login
@app.route('/login')
def login():
    return render_template('/login.html')


# new category
@app.route('/category/new')
def newCategory():
    return render_template('/newcategory.html')


# edit category
@app.route('/category/<int:category_id>/edit')
def editCategory(category_id):
    editedCategory = session.query(Category).filter_by(id=category_id).one()
    return render_template('/editcategory.html', category=editedCategory)


# delete category
@app.route('/category/<int:category_id>/delete')
def deleteCategory(category_id):
    deletedCategory = session.query(Category).filter_by(id=category_id).one()
    return render_template('/deletecategory.html', category=deletedCategory)


# show books in one category
@app.route('/category/<int:category_id>/')
@app.route('/category/<int:category_id>/book')
def showBooks():
    return "This is the category page showing the book(s)"


# new book
@app.route('/book/new')
def newBook():
    return render_template('/newbook.html')


# edit book
@app.route('/category/<int:category_id>/book/<int:book_id>/edit')
def editBook(category_id, book_id):
    editedBook = session.query(Book).filter_by(id=book_id).one()
    # category = session.query(Category).filter_by(id=category_id).one()
    return render_template('/editbook.html', category_id=category_id,
                           book_id=book_id, book=editedBook)


# delete book
@app.route('/category/<int:category_id>/book/<int:book_id>/delete')
def deleteBook(category_id, book_id):
    deletedBook = session.query(Book).filter_by(id=book_id).one()
    # category = session.query(Category).filter_by(id=category_id).one()
    return render_template('/deletebook.html', category_id=category_id,
                           book_id=book_id, book=deletedBook)
# [END Routes]


# Flask
if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
