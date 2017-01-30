"""
Helper methods with creating users and getting user info
"""

# [START Imports]
from database import db_session, User
# [END Imports]


# [START User Helper Methods]
def createUser(login_session):
    """
    Creates new user in the db based on OAuth profile info.
    login_session is passed in, and this info is used to create and persist
    a user in the db.
    Output is the user.id of the newly created user
    """
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    db_session.add(newUser)
    db_session.commit()
    user = db_session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    """
    If a user_id is passed into this method, it returns the
    user object associated with the id
    """
    user = db_session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    """
    Takes in an email address, and if this matches a value stored in
    db, it returns the associated user.id
    """
    try:
        user = db_session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None
# [END User Helper Methods]
