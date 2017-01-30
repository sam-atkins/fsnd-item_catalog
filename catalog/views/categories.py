"""
CRUD operations and views for categories
Blueprint: category_admin
"""

# [START Imports]
# Flask & others
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask import session as login_session

# SQLAlchemy
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker

# Helpers
from catalog.forms import CategoryForm

# Db
from catalog.database import db_session, Category, Book
# [END Imports]


category_admin = Blueprint('category_admin', __name__)


# [START Database set-up]
# engine = create_engine(
#     'sqlite:////vagrant/fsnd-item_catalog/catalog/cataloguebooksv2.db')

# Base.metadata.bind = engine

# DBSession = sessionmaker(bind=engine)
# session = DBSession()
# [END Database set-up]


# [START Routes]
# show one categgry and all books in the category
@category_admin.route('/category/<int:category_id>/')
def showCategory(category_id):
    category = db_session.query(Category).filter_by(id=category_id).one()
    books = db_session.query(Book).filter_by(category_id=category_id).all()
    return render_template('categorybooks.html',
                           category_id=category_id, category=category,
                           books=books)


# new category
@category_admin.route('/category/new', methods=['GET', 'POST'])
def newCategory():
    # if 'username' not in login_session:
    #     return redirect('/login')
    form = CategoryForm(request.form)
    if request.method == 'POST' and form.validate():
        newCategory = Category(name=request.form['name'])  #,
                               # user_id=login_session['user_id'])
        db_session.add(newCategory)
        db_session.commit()
        flash('New Category %s Successfully Created' % newCategory.name)
        return redirect(url_for('homePage.index'))
    return render_template('/newcategory.html', form=form)


# edit category
@category_admin.route('/category/<int:category_id>/edit',
                      methods=['GET', 'POST'])
def editCategory(category_id):
    editedCategory = db_session.query(Category).filter_by(id=category_id).one()
    form = CategoryForm(request.form)
    # if 'username' not in login_session:
    #     return redirect('/login')
    # if editedCategory.user_id != login_session['user_id']:
    #     flash('You are not authorised to edit this category.')
    # return redirect(url_for('book_admin.showBooks', category_id=category_id))
    if request.method == 'POST' and form.validate():
        editedCategory.name = request.form['name']
        db_session.add(editedCategory)
        db_session.commit()
        flash('Category %s Successfully Edited' % editedCategory.name)
        return redirect(url_for('homePage.index'))
    else:
        return render_template('/editcategory.html', category=editedCategory,
                               form=form)


# delete category
@category_admin.route('/category/<int:category_id>/delete',
                      methods=['GET', 'POST'])
def deleteCategory(category_id):
    deletedCategory = db_session.query(
        Category).filter_by(id=category_id).one()
    # if 'username' not in login_session:
    #     return redirect('/login')
    # if deletedCategory.user_id != login_session['user_id']:
    #     flash('You are not authorised to delete this category.')
    # return redirect(url_for('book_admin.showBooks', category_id=category_id))
    if request.method == 'POST':
        db_session.delete(deletedCategory)
        db_session.commit()
        flash('Category %s successfully deleted!' % deletedCategory.name)
        return redirect(url_for('homePage.index'))
    else:
        return render_template('/deletecategory.html',
                               category=deletedCategory)
# [END Routes]
