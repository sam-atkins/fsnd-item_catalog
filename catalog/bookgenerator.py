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

category4 = Category(name="Sport", user=user2)
db_session.add(category4)
db_session.commit()

category5 = Category(name="Thrillers", user=user1)
db_session.add(category5)
db_session.commit()

category6 = Category(name="Nature", user=user2)
db_session.add(category6)
db_session.commit()

category7 = Category(name="Business", user=user1)
db_session.add(category7)
db_session.commit()


# Add Autobiography books; remove user if dev 1
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
                 description="Practical programming for total beginners. In "
                 "Automate the Boring Stuff with Python, you'll learn how to "
                 "use Python to write programs that do in minutes what would "
                 "take you hours to do by hand-no prior programming "
                 "experience required.",
                 author="Al Sweigart", price="14.99", category=category2,
                 user=user1)
db_session.add(bookItem2)
db_session.commit()

bookItem3 = Book(name="Javascript and jQuery",
                 description="Welcome to a nicer way to learn Javascript "
                 "& jQuery",
                 author="John Duckett", price="19.99", category=category2,
                 user=user1)
db_session.add(bookItem3)
db_session.commit()

bookItem4 = Book(name="Learn Python the Hard Way",
                 description="Zed Shaw has perfected the world's best "
                 "system for learning Python. Follow it and you will "
                 "succeed-just like the hundreds of thousands of beginners "
                 "Zed has taught to date! You bring the discipline, "
                 "commitment, and persistence; the author supplies "
                 "everything else. ",
                 author="Zed Shaw", price="18.99", category=category2,
                 user=user1)
db_session.add(bookItem4)
db_session.commit()

bookItem5 = Book(name="Python for Data Analysis",
                 description="Python for Data Analysis is concerned with "
                 "the nuts and bolts of manipulating, processing, cleaning, "
                 "and crunching data in Python. It is also a practical, "
                 "modern introduction to scientific computing in Python, "
                 "tailored for data-intensive applications.",
                 author="Wes McKinney", price="9.99", category=category2,
                 user=user1)
db_session.add(bookItem5)
db_session.commit()

bookItem6 = Book(name="Hacking: Beginner to Expert Guide",
                 description="This book will teach you how you can protect "
                 "yourself from most common hacking attacks -- by knowing "
                 "how hacking actually works!",
                 author="James Patterson", price="1.99", category=category2,
                 user=user2)
db_session.add(bookItem6)
db_session.commit()

bookItem7 = Book(name="Make Your Own Neural Network",
                 description="A step-by-step gentle journey through the "
                 "mathematics of neural networks, and making your own "
                 "using the Python computer language.",
                 author="Tariq Rashid", price="24.99", category=category2,
                 user=user1)
db_session.add(bookItem7)
db_session.commit()

# Add sci fi books; remove user if dev 1
bookItem8 = Book(name="Wool",
                 description="Thousands of them have lived underground."
                 "They've lived there so long, there are only legends about "
                 "people living anywhere else. Such a life requires rules. "
                 "Strict rules. There are things that must not be discussed. "
                 "Like going outside. Never mention you might like going "
                 "outside.",
                 author="Hugh Howey",
                 price="3.99", category=category3, user=user2)
db_session.add(bookItem8)
db_session.commit()


# Add thriller books; remove user if dev 1
bookItem9 = Book(name="Night School: A Jack Reacher Novel",
                 description="It is 1996, and Reacher is still in the army.",
                 author="Lee Child", price="7.99", category=category5,
                 user=user1)
db_session.add(bookItem9)
db_session.commit()

bookItem10 = Book(name="The Girl on the Train",
                  description="Rachel catches the same commuter train every "
                  "morning. She knows it will wait at the same signal each "
                  "time, overlooking a row of back gardens. She is even "
                  "started to feel like she knows the people who live in "
                  "one of the houses. Jess and Jason, she calls them. "
                  "Their life, as she sees it, is perfect. "
                  "If only Rachel could be that happy.",
                  author="Paula Hawkins", price="4.99", category=category5,
                  user=user1)
db_session.add(bookItem10)
db_session.commit()
