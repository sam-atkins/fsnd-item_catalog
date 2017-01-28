"""
CRUD operations and views for books
"""

# [START Imports]
# Flask & others
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask import session as login_session

# SQLAlchemy
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker

# Helpers
from catalog.forms import BookForm

# Db
from catalog.models import Base, Category, Book
# [END Imports]


books = Blueprint('books', __name__)


# [START Database set-up]
engine = create_engine(
    'sqlite:////vagrant/fsnd-item_catalog/catalog/cataloguebooksv2.db')

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()
# [END Database set-up]


# [START Routes]
# new book
@books.route('/book/new', methods=['GET', 'POST'])
def newBook():
    categories = session.query(Category).order_by(asc(Category.name))
    form = BookForm(request.form)
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST' and form.validate():
        c = request.form['category']
        c_submitted = session.query(Category).filter(
            Category.name == c).first()
        newBook = Book(name=request.form['name'],
                       description=request.form['description'],
                       price=request.form['price'],
                       author=request.form['author'],
                       category=c_submitted,
                       user_id=login_session['user_id'])
        session.add(newBook)
        session.commit()
        flash('New Book %s by %s Successfully Created' %
              (newBook.name, newBook.author))

        # amend redirect
        return redirect(url_for('index'))
    return render_template('/newbook.html', categories=categories, form=form)


# edit book
@books.route('/category/<int:category_id>/book/<int:book_id>/edit',
             methods=['GET', 'POST'])
def editBook(category_id, book_id):
    editedBook = session.query(Book).filter_by(id=book_id).one()
    categories = session.query(Category).order_by(asc(Category.name))
    form = BookForm(request.form)
    if 'username' not in login_session:
        return redirect('/login')
    if editedBook.user_id != login_session['user_id']:
        flash('You are not authorised to edit this book.')
        return redirect(url_for('showBooks', category_id=category_id))
    if request.method == 'POST' and form.validate():

        if request.form['name']:
            editedBook.name = request.form['name']
        if request.form['author']:
            editedBook.author = request.form['author']
        if request.form['price']:
            editedBook.price = request.form['price']
        if request.form['description']:
            editedBook.description = request.form['description']
        if request.form['category']:
            c = request.form['category']
            c_submitted = session.query(Category).filter(
                Category.name == c).first()
            editedBook.category = c_submitted

        session.add(editedBook)
        session.commit()

        flash('Book %s by %s Edited Successfully!' %
              (editedBook.name, editedBook.author))
        return redirect(url_for('index'))
    else:
        return render_template('/editbook.html', category_id=category_id,
                               book_id=book_id, book=editedBook,
                               categories=categories, form=form)


# delete book
@books.route('/category/<int:category_id>/book/<int:book_id>/delete',
             methods=['GET', 'POST'])
def deleteBook(category_id, book_id):
    deletedBook = session.query(Book).filter_by(id=book_id).one()
    if 'username' not in login_session:
        return redirect('/login')
    if deletedBook.user_id != login_session['user_id']:
        flash('You are not authorised to delete this book.')
        return redirect(url_for('showBooks', category_id=category_id))
    if request.method == 'POST':
        session.delete(deletedBook)
        session.commit()
        flash('Book %s by %s successfully deleted!' %
              (deletedBook.name, deletedBook.author))
        return redirect(url_for('index'))
    else:
        return render_template('/deletebook.html', category_id=category_id,
                               book_id=book_id, book=deletedBook)
# [END Routes]
