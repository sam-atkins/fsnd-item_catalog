"""
Classes to enable helper methods to validate form entry by users
"""

# [START Imports]
from wtforms import Form, StringField, validators
from flask import session
from wtforms.csrf.session import SessionCSRF
# import config

# [END Imports]


# [START Form Validation]
class BaseForm(Form):
    class Meta:
        csrf = True
        csrf_class = SessionCSRF
        csrf_secret = b'top_secret'

        @property
        def csrf_context(self):
            return session


class CategoryForm(BaseForm):
    """
    validates new category form to ensure an entry is made
    """
    name = StringField('name', [validators.Length(min=1, max=250)])


class BookForm(BaseForm):
    """
    validates new book form to ensure entries are made in each field
    """
    name = StringField('name', [validators.Length(min=1, max=250)])
    description = StringField(
        'description', [validators.Length(min=5, max=750)])
    author = StringField('author', [validators.Length(min=5, max=250)])
    price = StringField('price', [validators.Length(min=1, max=8)])
# [END Form Validation]
