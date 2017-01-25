"""
Populates the db with some data
Used for dev purposes
"""

# [START imports]
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Category, Book
# [END imports]

# [START Db engine and session]
engine = create_engine('sqlite:///cataloguebooks.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()

session = DBSession()
# [END Db engine and session]

# Add categories
category1 = Category(name="Autobiography")
session.add(category1)
session.commit()

category2 = Category(name="Web Development")
session.add(category2)
session.commit()

category3 = Category(name="Science Fiction")
session.add(category3)
session.commit()

# Add business books
bookItem1 = Book(name="Steve Jobs: A Biography",
                 description="Driven by demons, Jobs could drive those around "
                 "him to fury and despair. But his personality and products "
                 "were interrelated, just as Apples hardware and software "
                 "tended to be, as if part of an integrated system. His tale "
                 "is instructive and cautionary, filled with lessons about "
                 "innovation, character, leadership, and values.",
                 author="Walter Isaacson",
                 price="9.99", category=category1)
session.add(bookItem1)
session.commit()


# Add web dev books
bookItem2 = Book(name="Automate the Boring Stuff",
                 description="Learn Python 3...",
                 author="Al Sweigart", price="14.99", category=category2)
session.add(bookItem2)
session.commit()

# Add thriller books
bookItem3 = Book(name="Wool",
                 description="Thousands of them have lived underground."
                 "They've lived there so long, there are only legends about "
                 "people living anywhere else. Such a life requires rules. "
                 "Strict rules. There are things that must not be discussed. "
                 "Like going outside. Never mention you might like going "
                 "outside.",
                 author="Hugh Howey",
                 price="3.99", category=category3)
session.add(bookItem3)
session.commit()
