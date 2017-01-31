"""
CRUD operations and views for books
Blueprint: book_admin
"""

# [START Imports]
# Flask & others
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask import session as login_session

# SQLAlchemy
from sqlalchemy import asc

# Helpers
from catalog.forms import BookForm

# Db
from catalog.database import db_session, Category, Book
# [END Imports]


book_admin = Blueprint('book_admin', __name__)


# [START Routes]
# display one book
@book_admin.route('/category/<int:category_id>/book/<int:book_id>')
def theBook(category_id, book_id):
    """Displays page showing one book including all the book's info"""
    book = db_session.query(Book).filter_by(id=book_id).one()
    return render_template('book.html', category_id=category_id, book=book)


# new book
@book_admin.route('/book/new', methods=['GET', 'POST'])
def newBook():
    """Create a new book, with control that user must be logged in

    """
    categories = db_session.query(Category).order_by(asc(Category.name))
    form = BookForm(request.form)
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST' and form.validate():
        c = request.form['category']
        c_submitted = db_session.query(Category).filter(
            Category.name == c).first()
        newBook = Book(name=request.form['name'],
                       description=request.form['description'],
                       price=request.form['price'],
                       author=request.form['author'],
                       category=c_submitted,
                       user_id=login_session['user_id'])
        db_session.add(newBook)
        db_session.commit()
        flash('New Book %s by %s Successfully Created' %
              (newBook.name, newBook.author))

        return redirect(url_for('homePage.index'))
    return render_template('/newbook.html', categories=categories, form=form)


# edit book
@book_admin.route('/category/<int:category_id>/book/<int:book_id>/edit',
                  methods=['GET', 'POST'])
def editBook(category_id, book_id):
    """Edit a book, with local permissions:
    User must be logged in and created of the original book entry
    """
    editedBook = db_session.query(Book).filter_by(id=book_id).one()
    categories = db_session.query(Category).order_by(asc(Category.name))
    form = BookForm(request.form)
    if 'username' not in login_session:
        return redirect('/login')
    if editedBook.user_id != login_session['user_id']:
        flash('You are not authorised to edit this book.')
        return redirect(url_for('category_admin.showCategory',
                                category_id=category_id))
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
            c_submitted = db_session.query(Category).filter(
                Category.name == c).first()
            editedBook.category = c_submitted

        db_session.add(editedBook)
        db_session.commit()

        flash('Book %s by %s Edited Successfully!' %
              (editedBook.name, editedBook.author))
        return redirect(url_for('homePage.index'))
    else:
        return render_template('/editbook.html', category_id=category_id,
                               book_id=book_id, book=editedBook,
                               categories=categories, form=form)


# delete book
@book_admin.route('/category/<int:category_id>/book/<int:book_id>/delete',
                  methods=['GET', 'POST'])
def deleteBook(category_id, book_id):
    """Manages book deletion. Local Permissions:
    Must be logged in and user that created the book"""
    deletedBook = db_session.query(Book).filter_by(id=book_id).one()
    form = BookForm(request.form)
    if 'username' not in login_session:
        return redirect('/login')
    if deletedBook.user_id != login_session['user_id']:
        flash('You are not authorised to delete this book.')
        return redirect(url_for('category_admin.showCategory',
                                category_id=category_id))
    if request.method == 'POST':
        db_session.delete(deletedBook)
        db_session.commit()
        flash('Book %s by %s successfully deleted!' %
              (deletedBook.name, deletedBook.author))
        return redirect(url_for('homePage.index'))
    else:
        return render_template('/deletebook.html', category_id=category_id,
                               book_id=book_id, book=deletedBook, form=form)
# [END Routes]
