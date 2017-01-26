"""
Helper methods to validate form entry by users
"""

# [START Imports]
from wtforms import Form, StringField, validators
# [END Imports]


# [START Form Validation]
class CategoryForm(Form):
    """
    validates new category form to ensure an entry is made
    """
    name = StringField('name', [validators.Length(min=1, max=250)])


class BookForm(Form):
    """
    validates new book form to ensure entries are made in each field
    """
    name = StringField('name', [validators.Length(min=1, max=250)])
    description = StringField(
        'description', [validators.Length(min=5, max=250)])
    author = StringField('author', [validators.Length(min=5, max=250)])
    price = StringField('price', [validators.Length(min=1, max=8)])
# [END Form Validation]
