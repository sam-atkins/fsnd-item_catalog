"""
Decorator
- login_required checks if user is logged in
"""

# [START Imports]
from functools import wraps
from flask import redirect
from flask import session as login_session
# [END Imports]


def login_required(function):
    """Validates if a user is logged in, if not
    redirect to login page
    """
    @wraps(function)
    def wrapper(*args, **kwargs):
        if 'username' not in login_session:
            return redirect('/login')
        else:
            return function(*args, **kwargs)
    return wrapper
