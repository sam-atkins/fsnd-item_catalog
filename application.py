"""
Application docstrings here
"""

# [START Imports]
# Flask & others
from flask import Flask, render_template, request, redirect, url_for, flash, \
    jsonify
from flask_wtf.csrf import CSRFProtect
from flask import session as login_session
import random
import string

# OAuth
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
from flask import make_response
import httplib2
import requests
import json

# SQLAlchemy
from sqlalchemy import create_engine, asc, desc
from sqlalchemy.orm import sessionmaker

# Helpers
from forms import CategoryForm, BookForm
from userhelp import createUser, getUserID

# Db
from database_setup import Base, Category, Book
# [END Imports]


CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Book Catalogue App"


# [START Database set-up]
engine = create_engine('sqlite:///cataloguebooksv2.db')
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
# login
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    return render_template('login.html', STATE=state)


# OAuth Google Plus - gconnect
@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps(
            'Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    # ADD PROVIDER TO LOGIN SESSION
    login_session['provider'] = 'google'

    # see if user exists, if it doesn't make a new one
    user_id = getUserID(data["email"])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    # refactor after testing to 'login loading' page
    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output


# OAuth disconnect - gdisconnect
@app.route('/gdisconnect')
def gdisconnect():
    # Only disconnect a connected user.
    credentials = login_session.get('credentials')
    if credentials is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = credentials.access_token
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] != '200':
        # For whatever reason, the given token was invalid.
        response = make_response(
            json.dumps('Failed to revoke token for given user.'), 400)
        response.headers['Content-Type'] = 'application/json'
        return response


# Disconnect based on provider; enables disconnect from multiple providers
@app.route('/disconnect')
def disconnect():
    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            gdisconnect()
            del login_session['gplus_id']
            del login_session['access_token']
        # if login_session['provider'] == 'provider_name':
        #     provider_namedisconnect()
        #     del login_session['provider_name']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        del login_session['provider']
        flash("You have successfully been logged out.")
        return redirect(url_for('index'))
    else:
        flash("You were not logged in")
        return redirect(url_for('index'))


# Home /index
@app.route('/')
@app.route('/catalogue')
def index():
    categories = session.query(Category).order_by(asc(Category.name))
    books = session.query(Book).order_by(desc(Book.created_at))
    return render_template('index.html', categories=categories, books=books)


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


# new category
@app.route('/category/new', methods=['GET', 'POST'])
def newCategory():
    if 'username' not in login_session:
        return redirect('/login')
    form = CategoryForm(request.form)
    if request.method == 'POST' and form.validate():
        newCategory = Category(name=request.form['name'],
                               user_id=login_session['user_id'])
        session.add(newCategory)
        session.commit()
        flash('New Category %s Successfully Created' % newCategory.name)
        return redirect(url_for('index'))
    return render_template('/newcategory.html', form=form)


# edit category
@app.route('/category/<int:category_id>/edit', methods=['GET', 'POST'])
def editCategory(category_id):
    editedCategory = session.query(Category).filter_by(id=category_id).one()
    form = CategoryForm(request.form)
    if 'username' not in login_session:
        return redirect('/login')
    if editedCategory.user_id != login_session['user_id']:
        flash('You are not authorised to edit this category.')
        return redirect(url_for('showBooks', category_id=category_id))
    if request.method == 'POST' and form.validate():
        editedCategory.name = request.form['name']
        session.add(editedCategory)
        session.commit()
        flash('Category %s Successfully Edited' % editedCategory.name)
        return redirect(url_for('index'))
    else:
        return render_template('/editcategory.html', category=editedCategory,
                               form=form)


# delete category
@app.route('/category/<int:category_id>/delete', methods=['GET', 'POST'])
def deleteCategory(category_id):
    deletedCategory = session.query(Category).filter_by(id=category_id).one()
    if 'username' not in login_session:
        return redirect('/login')
    if deletedCategory.user_id != login_session['user_id']:
        flash('You are not authorised to delete this category.')
        return redirect(url_for('showBooks', category_id=category_id))
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
@app.route('/category/<int:category_id>/book/<int:book_id>/edit',
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
@app.route('/category/<int:category_id>/book/<int:book_id>/delete',
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


# [START JSON API Endpoints]
@app.route('/categories/JSON')
def allCategoriesJSON():
    categories = session.query(Category).all()
    return jsonify(categories=[c.serialize for c in categories])


@app.route('/book/<int:book_id>/JSON')
def bookJSON(book_id):
    book = session.query(Book).filter_by(id=book_id).one()
    return jsonify(book=book.serialize)


@app.route('/category/<int:category_id>/JSON')
def categoryWithBooksJSON(category_id):
    books = session.query(Book).filter_by(id=category_id).all()
    return jsonify(Category=[b.serialize for b in books])
# [END JSON API Endpoints]


# Flask
if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
