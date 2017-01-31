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


## Set-Up Instructions

### Summary

1. Requirements 
2. Configuration
3. Vagrant
4. Database set-up
5. Run Time


#### 1. Requirements

This app was built using a Vagrant Virtual Box and runs on Python 2 using the Flask Microframework. 

In addition to Flask, key packages include WTForms and SQLAlchemy.

#### 2. Configuration

There are two files which need to be configured. 

First, the `config.py` file is located in the repo root directory. Consider adding an `APP_SECRET_KEY` and a `CSRF_SECRET_KEY`, and if applicable add the `config.py` file to `.gitignore

Example `config.py` file below:

```
APP_SECRET_KEY = 'add_a_super_secret_key'
app_debug = True
app_run_host = '0.0.0.0'
app_run_port = port = 8000
CSRF_SECRET_KEY = b'add_a_top_secret_key'
```

Second, is the `client_secrets.json` file. This should also be saved in the repo root directory. This should include the Google OAuth API information.

See this link for Google info:

[Using OAuth 2.0 to Access Google APIs - Google Developers](https://developers.google.com/identity/protocols/OAuth2)

The file will look like this. Add in your `client_id` and `client_secret`.

If you are using a different port than 8000 for dev, change this in your Google OAuth API App settings and in the JSON file.

```
{
    "web": {
        "client_id": "ADD_CLIENT_ID",
        "project_id": "book-catalogue-app",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://accounts.google.com/o/oauth2/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_secret": "ADD_SECRET",
        "redirect_uris": ["http://localhost:8000"],
        "javascript_origins": ["http://localhost:8000"]
    }
}
```


#### 3. Vagrant

Next, fire up Vagrant.

Move to the project folder e.g.:
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

# alternatively, just do this
$ cd /vagrant/fsnd-item_catalog
```

For later on, to exit/stop Vagrant:
```
# to exit the virtual box:
$ exit

# to stop Vagrant and not lose any data
$ vagrant halt
```


#### 4. Database set-up

Once Vagrant is up and you are in the project repo, here’s how to set-up the database:

```
# move to the catalog folder
$ cd catalog

# execute the bookgenerator file
# this populates the database with some initial data
$ python bookgenerator.py
```



#### 4. Run Time

Ensure you are back in the root directory and then enter the command `run.py`. The app server will launch. Navigate to `localhost:8000` in your browser to see the app.


## Demo
This project is not live so screenshots are included below:

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

**API JSON - Book**
![API JSON Book](/docs/json_book.png?raw=true "API JSON Book")
