"""
Application docstrings here
"""

# [START Imports]
# Flask
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_wtf.csrf import CSRFProtect

# SQLAlchemy
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker

# Helpers
from forms import CategoryForm, BookForm

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
csrf = CSRFProtect()


def create_app():
    app = Flask(__name__)
    csrf.init_app(app)


# [START Routes]
# Home /index
@app.route('/')
@app.route('/catalogue')
def index():
    categories = session.query(Category).order_by(asc(Category.name))
    return render_template('index.html', categories=categories)


# show books in one category
@app.route('/category/<int:category_id>/')
def showBooks(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    books = session.query(Book).filter_by(category_id=category_id).all()
    return render_template('/categorybooks.html',
                           category_id=category_id, category=category,
                           books=books)


# display one book
@app.route('/book/<int:book_id>')
def theBook(book_id):
    book = session.query(Book).filter_by(id=book_id).one()
    return render_template('/book.html', book=book)


# login
@app.route('/login')
def login():
    return render_template('/login.html')


# new category
@app.route('/category/new', methods=['GET', 'POST'])
def newCategory():
    form = CategoryForm(request.form)
    if request.method == 'POST' and form.validate():
        newCategory = Category(name=request.form['name'])
        session.add(newCategory)
        session.commit()
        flash('New Category %s Successfully Created' % newCategory.name)

        # change redirect
        return redirect(url_for('index'))
    return render_template('/newcategory.html', form=form)
    # return render_template('/newcategoryv2.html', form=form)


# edit category
@app.route('/category/<int:category_id>/edit', methods=['GET', 'POST'])
def editCategory(category_id):
    editedCategory = session.query(Category).filter_by(id=category_id).one()
    if request.method == 'POST':
        editedCategory.name = request.form['category']
        session.add(editedCategory)
        session.commit()
        flash('Category %s Successfully Edited' % editedCategory.name)
        return redirect(url_for('index'))
    return render_template('/editcategory.html', category=editedCategory)


# delete category
@app.route('/category/<int:category_id>/delete', methods=['GET', 'POST'])
def deleteCategory(category_id):
    deletedCategory = session.query(Category).filter_by(id=category_id).one()
    if request.method == 'POST':
        session.delete(deletedCategory)
        session.commit()
        flash('Category %s successfully deleted!' % deletedCategory.name)
        return redirect(url_for('index'))
    else:
        return render_template('/deletecategory.html',
                               category=deletedCategory)


# new book
@app.route('/book/new', methods=['GET', 'POST'])
def newBook():
    categories = session.query(Category).order_by(asc(Category.name))
    form = BookForm(request.form)
    if request.method == 'POST' and form.validate():
        c = request.form['category']
        c_submitted = session.query(Category).filter(
            Category.name == c).first()
        newBook = Book(name=request.form['name'],
                       description=request.form['description'],
                       price=request.form['price'],
                       author=request.form['author'],
                       category=c_submitted)
        session.add(newBook)
        session.commit()
        flash('New Book %s by %s Successfully Created' %
              (newBook.name, newBook.author))

        # amend redirect
        return redirect(url_for('index'))
    return render_template('/newbookv2.html', categories=categories, form=form)


# new book - no form validation
# @app.route('/book/new', methods=['GET', 'POST'])
# def newBook():
#     categories = session.query(Category).order_by(asc(Category.name))
#     if request.method == 'POST':
#         c = request.form['category']
#         c_submitted = session.query(Category).filter(
#             Category.name == c).first()
#         newBook = Book(name=request.form['name'],
#                        description=request.form['description'],
#                        price=request.form['price'],
#                        author=request.form['author'],
#                        category=c_submitted)
#         session.add(newBook)
#         session.commit()
#         flash('New Book %s by %s Successfully Created' %
#               (newBook.name, newBook.author))

#         # amend redirect
#         return redirect(url_for('index'))
#     return render_template('/newbook.html', categories=categories)


# edit book
@app.route('/category/<int:category_id>/book/<int:book_id>/edit',
           methods=['GET', 'POST'])
def editBook(category_id, book_id):
    editedBook = session.query(Book).filter_by(id=book_id).one()
    # category = session.query(Category).filter_by(id=category_id).one()
    categories = session.query(Category).order_by(asc(Category.name))
    if request.method == 'POST':

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
                               categories=categories)


# delete book
@app.route('/category/<int:category_id>/book/<int:book_id>/delete',
           methods=['GET', 'POST'])
def deleteBook(category_id, book_id):
    deletedBook = session.query(Book).filter_by(id=book_id).one()
    # category = session.query(Category).filter_by(id=category_id).one()
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


# Flask
if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
