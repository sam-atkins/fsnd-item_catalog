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
This project is not live so screenshots are included below:

![add_category](/fsnd-item_catalog/blob/master/docs/addcategory.png?raw=true "Optional Title")

![add_category](cubiio/fsnd-item_catalog/blob/master/docs/addcategory.png?raw=true "Optional Title")

![add_category](/blob/master/docs/addcategory.png?raw=true "Optional Title")

![Add Category](https://github.com/cubiio/fsnd-item_catalog/blob/master/docs/addcategory.png)
