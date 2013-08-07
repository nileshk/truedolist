True Do List
============

This is a simple todo list web application written using Django and
jQuery. The back end exposes JSON services.  The UI is mostly
JavaScript calling those services (no use of Django templates at the
moment and only a small amount of static HTML).

It is currently a work in progress.  However, it is functional at the
moment, though lacking some polish.  I am in the middle of developing
the "label" feature.  And the JSON services could probably be made
more RESTful and the API for is subject to change.

Why another todo list?
----------------------

Why did I create yet another todo list?  Most todo list web apps out
there are either too complicated with a lot of features I don't use or
way too simple.  Some come close to doing exactly what I want, but
either have a cluttered interface, require a subscription, or don't
have a fully functional phone version.  So I decided to create my own.
Actually the first iteration of this was written in Java and I am
still using that [version](http://github.com/nileshk/truedolist-java).
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
* Highlight an item

I am planning to add these features:

* Use various different colors for highlighting
* Strikethrough an item (to signify it is done)
    
Prerequisites
-------------

* Python 2.7 or higher 2.x version
* [Django 1.6](http://www.djangoproject.com/) or higher
* [South 0.8.1](http://south.aeracode.org/) (Optional for DB migrations)
* [Blueprint CSS Framework](http://www.blueprintcss.org/)

Uses CDN for
------------
* [jQuery](http://jquery.com/)
* [jQuery UI](http://jqueryui.com/)

Setup
-----

For the web UI to work:

* Run `scripts/setup.sh` which will download Blueprint and copy its `blueprint` folder into `static/css`

The project is currently configured to use an sqlite3 database, but
you should be able to configure whatever database you want (I have not
used any database specific code, though if I do, it will be for PostgreSQL).

There currently is no login page, so you will need to login through
the admin application first and then navigate to `/static/index.html`.

Credits
-------

All code was written by [Nilesh Kapadia](http://www.nileshk.com)
except for `http_basic.py`.  I lost track of where I obtained
`http_basic.py` from, if anyone recognizes it, please let me know so I
can give credit to the source.
