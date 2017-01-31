"""
CRUD operations and views for categories
Blueprint: category_admin
"""

# [START Imports]
# Flask & others
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask import session as login_session

# Helpers
from catalog.forms import CategoryForm
from catalog.decorators import login_required

# Db
from catalog.database import db_session, Category, Book
# [END Imports]


category_admin = Blueprint('category_admin', __name__)


# [START Routes]
# show one categgry and all books in the category
@category_admin.route('/category/<int:category_id>/')
def showCategory(category_id):
    """Displays the category with all books within the category"""
    category = db_session.query(Category).filter_by(id=category_id).one()
    books = db_session.query(Book).filter_by(category_id=category_id).all()
    return render_template('categorybooks.html',
                           category_id=category_id, category=category,
                           books=books)


# new category
@category_admin.route('/category/new', methods=['GET', 'POST'])
@login_required
def newCategory():
    """Allows a logged in user to create a new category"""
    form = CategoryForm(request.form)
    if request.method == 'POST' and form.validate():
        new_category = Category(name=request.form['name'],
                                user_id=login_session['user_id'])
        db_session.add(new_category)
        db_session.commit()
        flash('New Category %s Successfully Created' % new_category.name)
        return redirect(url_for('homePage.index'))
    return render_template('/newcategory.html', form=form)


# edit category
@category_admin.route('/category/<int:category_id>/edit',
                      methods=['GET', 'POST'])
@login_required
def editCategory(category_id):
    """Allows a category to be edited, with local permissions:
    user must be logged in and original creator of the category
    """
    editedCategory = db_session.query(Category).filter_by(id=category_id).one()
    form = CategoryForm(request.form)
    if editedCategory.user_id != login_session['user_id']:
        flash('You are not authorised to edit this category.')
        return redirect(url_for('category_admin.showCategory',
                                category_id=category_id))
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
@login_required
def deleteCategory(category_id):
    """Allows a category to be deleted, with local permissions:
    user must be logged in and original creator of the category
    """
    deletedCategory = db_session.query(
        Category).filter_by(id=category_id).one()
    form = CategoryForm(request.form)
    if deletedCategory.user_id != login_session['user_id']:
        flash('You are not authorised to delete this category.')
        return redirect(url_for('category_admin.showCategory',
                                category_id=category_id))
    if request.method == 'POST':
        db_session.delete(deletedCategory)
        db_session.commit()
        flash('Category %s successfully deleted!' % deletedCategory.name)
        return redirect(url_for('homePage.index'))
    else:
        return render_template('/deletecategory.html',
                               category=deletedCategory, form=form)
# [END Routes]
