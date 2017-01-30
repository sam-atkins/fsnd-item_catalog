"""
Populates the db with some data
Used for dev purposes
"""

# [START imports]
from database import db_session, User, Category, Book
# [END imports]


# Add User
user1 = User(name="Mr. Clement DuBuque", email="CDubuque@Ullrich.net")
db_session.add(user1)
db_session.commit()

user2 = User(name="Tressie Bernier", email="Tressie.Bernier@gmail.com")
db_session.add(user2)
db_session.commit()


# Add categories no users = dev 1
# category1 = Category(name="Autobiography")
# db_session.add(category1)
# db_session.commit()

# category2 = Category(name="Web Development")
# db_session.add(category2)
# db_session.commit()

# category3 = Category(name="Science Fiction")
# db_session.add(category3)
# db_session.commit()


# Add categories with users = dev 2
category1 = Category(name="Autobiography", user=user1)
db_session.add(category1)
db_session.commit()

category2 = Category(name="Web Development", user=user1)
db_session.add(category2)
db_session.commit()

category3 = Category(name="Science Fiction", user=user2)
db_session.add(category3)
db_session.commit()


# Add business books; remove user if dev 1
bookItem1 = Book(name="Steve Jobs: A Biography",
                 description="Driven by demons, Jobs could drive those around "
                 "him to fury and despair. But his personality and products "
                 "were interrelated, just as Apples hardware and software "
                 "tended to be, as if part of an integrated system. His tale "
                 "is instructive and cautionary, filled with lessons about "
                 "innovation, character, leadership, and values.",
                 author="Walter Isaacson",
                 price="9.99", category=category1, user=user1)
db_session.add(bookItem1)
db_session.commit()


# Add web dev books; remove user if dev 1
bookItem2 = Book(name="Automate the Boring Stuff",
                 description="Learn Python 3...",
                 author="Al Sweigart", price="14.99", category=category2,
                 user=user1)
db_session.add(bookItem2)
db_session.commit()

# Add thriller books; remove user if dev 1
bookItem3 = Book(name="Wool",
                 description="Thousands of them have lived underground."
                 "They've lived there so long, there are only legends about "
                 "people living anywhere else. Such a life requires rules. "
                 "Strict rules. There are things that must not be discussed. "
                 "Like going outside. Never mention you might like going "
                 "outside.",
                 author="Hugh Howey",
                 price="3.99", category=category3, user=user2)
db_session.add(bookItem3)
db_session.commit()
