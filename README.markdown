True Do List
============

This is a simple todo list application written using Django and
jQuery. The back end exposes JSON services.  The UI mostly JavaScript
calling those services (no use of Django templates at the moment and
only a small amount of static HTML).

It is currently a work in progress.  However, it is fully functional
at the moment.  I am in the middle of developing the "label" feature.
And the JSON services could probably be made more RESTful and the API
for is subject to change.

Why another todo list?
----------------------

Why did I create yet another todo list?  Most todo list web apps out
there are either too complicated with a lot of features I don't use or
way too simple.  Some come close to doing exactly what I want, but
either have a cluttered interface, require a subscription, or don't
have a fully functional phone version.  So I decided to create my
own.  Actually the first iteration of this was written in Java and I
am still using that version (which I intend to open source as well).
This is a rewrite of that.

Design
------

The design is very simple and you can do the following actions:

* Create multiple lists with a title
* Create items under a list.  Items are just plain text
* Rename lists or items
* Move items from one list to another
* Reorder lists
* Reorder items within lists
* Delete lists or items
* Create, rename, delete labels
* Apply labels to lists

I am planning to add these features:

* Highlight an item
* Strikethrough an item (to signify it is done)
    
Prerequisites
-------------

* Python 2.5 or higher 2.x version
* [Django 1.1](http://www.djangoproject.com/)
* [South 0.6](http://south.aeracode.org/) (Optional for DB migrations)
* [Blueprint CSS Framework](http://www.blueprintcss.org/)
* [jQuery](http://jquery.com/)
* [jQuery UI](http://jqueryui.com/)

Setup
-----

For the web UI to work:
* Create directories `static/js` and `static/css`
* Copy the `blueprint` folder into `static/css`
* Copy `jquery.js` into `static/js`
* Copy `jquery-ui.js` into `static/js`

The project is currently configured to use an sqlite3 database, but
you should be able to configure whatever database you want (I have not
used any database specific code, though if I do, it will be for PostgreSQL).

Credits
-------

All code was written by [Nilesh Kapadia](http://www.nileshk.com)
except for `http_basic.py`.  I lost track of where I obtained
`http_basic.py` from, if anyone recognizes it, please let me know so I
can give credit to the source.
