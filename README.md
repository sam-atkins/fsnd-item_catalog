# Item Catalog

## About this project

This project is part of my **Udacity FullStack NanoDegree**.

### Project specification:

* OAuth authentication and authorisation for users
* `CRUD` operations i.e. users can created, edit and delete Categories and Books
* Local permission systems for `CRUD` operations
* CSRF protection on `CRUD` operations
* API: JSON endpoints 

### Built with:

* Python
* Flask
* Jinja2 templates
* Bootstrap

### Status

**Submitted for Udacity code review**


## Instructions

### Application set-up and run

This app was built using a Vagrant Virtual Box and runs on Python 2 using the Flask Microframework. 

To run the app, fire up Vagrant (see info below), and enter the command `run.py`. The app server will launch. Navigate to localhost:8000 in your browser to see the app.

Note, ensure the app has a `config.py` in the repo root e.g.

```
app_debug = True
app_run_host = '0.0.0.0'
app_run_port = port = 8000

# also add secret stuff! 
```

You will also need a `client_secrets.json` with Google OAuth info including `client_id` and `client_secret`.

### Vagrant

Move to the project folder:
```
$ cd /vagrant/fsnd-item_catalog
```

Fire up Vagrant:
```
# load vagrant
$ vagrant up

# login via ssh
$ vagrant ssh
```

Once Vagrant is up:
```
# cd to the vagrant shared folder:
$ cd /vagrant

# then move to the project folder:
$ cd fsnd-item_catalog

# alternatively
$ cd /vagrant/fsnd-item_catalog
```

To exit/stop Vagrant:
```
$ exit
$ vagrant halt
```


## Demo
This project is not live (hosted) so screenshots are included below:

**Home Page**
![Home Page](/docs/homepage.png?raw=true "Home Page")

**Category Page**
![Category Page](/docs/categorypage.png?raw=true "Category Page")

**Book Page**
![Book Page](/docs/bookpage.png?raw=true "Book Page")

**Login**
![Login](/docs/login.png?raw=true "Login")

**Successful Login**
![Successful Login](/docs/success_login.png?raw=true "Successful Login")

**Add Category**
![Add Category](/docs/addcategory.png?raw=true "Add Category")

**Add Book**
![Add Book](/docs/addnewbook.png?raw=true "Add Book")

**Flash Messaging**
![Flash Messaging](/docs/flash_message.png?raw=true "Flash Messaging")

**Edit**
![Edit](/docs/editbook.png?raw=true "Edit")

**Delete**
![Delete](/docs/deletebook.png?raw=true "Delete")

**API JSON - Categories**
![API JSON Categories](/docs/json_categories.png?raw=true "API JSON Categories")

**API JSON - Category with books**
![API JSON Category with books](/docs/json_category_books.png?raw=true "API JSON Category with books")

**API JSON Book- **
![API JSON Book](/docs/json_book.png?raw=true "API JSON Book")
