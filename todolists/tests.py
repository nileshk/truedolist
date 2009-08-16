"""
Test for views
"""

__test__ = {"doctest": """

# Imports
>>> from models import TodoList, TodoItem
>>> from django.contrib.auth.models import User
>>> from django.test import Client
>>> from django.contrib.auth import authenticate, login
>>> from django.utils import simplejson as json

# Initialize
>>> client = Client()
>>> User.objects.all().delete()
>>> user1 = User.objects.create(username="test3")
>>> user1.set_password("pw")
>>> user1.save()
>>> client.login(username=user1.username, password="pw")
True

# Create Lists #

>>> r = client.post('/api/lists/', { 'title': 'list #1' })
>>> r.status_code
200
>>> json.loads(r.content)
{u'id': 1}

>>> r = client.post('/api/lists/', { 'title': 'list #2' })
>>> r.status_code
200
>>> json.loads(r.content)
{u'id': 2}

# Create Items #

>>> r = client.post('/api/lists/1/items/', { 'title': 'item #1' })
>>> r.status_code
200
>>> json.loads(r.content)
{u'id': 1}

>>> r = client.post('/api/lists/1/items/', { 'title': 'item #2' })
>>> r.status_code
200
>>> json.loads(r.content)
{u'id': 2}

>>> r = client.post('/api/lists/2/items/', { 'title': 'item #3' })
>>> r.status_code
200
>>> json.loads(r.content)
{u'id': 3}

>>> r = client.post('/api/lists/2/items/', { 'title': 'item #4' })
>>> r.status_code
200
>>> json.loads(r.content)
{u'id': 4}

>>> r = client.post('/api/lists/2/items/', { 'title': 'item #5' })
>>> r.status_code
200
>>> json.loads(r.content)
{u'id': 5}



# /api/lists/
>>> r = client.get('/api/lists/')
>>> r.status_code
200
>>> lists = json.loads(r.content)
>>> lists[0]
{u'position': 0, u'id': 1, u'title': u'list #1'}
>>> lists[1]
{u'position': 1, u'id': 2, u'title': u'list #2'}
>>> lists[0]['title']
u'list #1'
>>> lists[1]['title']
u'list #2'

>>> r = client.get('/api/lists/1/')
>>> r.status_code
200
>>> json.loads(r.content)
{u'position': 0, u'id': 1, u'title': u'list #1'}

>>> r = client.get('/api/lists/2/')
>>> r.status_code
200
>>> json.loads(r.content)
{u'position': 1, u'id': 2, u'title': u'list #2'}

>>> r = client.get('/api/lists/1/items/')
>>> r.status_code
200
>>> items = json.loads(r.content)
>>> items[0]
{u'position': 0, u'id': 1, u'title': u'item #1'}
>>> items[1]
{u'position': 1, u'id': 2, u'title': u'item #2'}

>>> r = client.get('/api/lists/2/items/')
>>> r.status_code
200
>>> items = json.loads(r.content)
>>> items[0]
{u'position': 0, u'id': 3, u'title': u'item #3'}
>>> items[1]
{u'position': 1, u'id': 4, u'title': u'item #4'}
>>> items[2]
{u'position': 2, u'id': 5, u'title': u'item #5'}

>>> r = client.get('/api/items/5/')
>>> r.status_code
200
>>> json.loads(r.content)
{u'position': 2, u'id': 5, u'title': u'item #5'}

>>> r = client.post('/api/lists/', { 'title': 'list #3' })
>>> r.status_code
200
>>> json.loads(r.content)
{u'id': 3}

>>> r = client.post('/api/lists/reposition/3/', { 'before_id': 1 })
>>> r.status_code
200
>>> json.loads(r.content)
{u'success': True}

# /api/lists/
>>> r = client.get('/api/lists/')
>>> r.status_code
200
>>> lists = json.loads(r.content)
>>> lists[0]
{u'position': 0, u'id': 3, u'title': u'list #3'}
>>> lists[1]
{u'position': 1, u'id': 1, u'title': u'list #1'}
>>> lists[2]
{u'position': 2, u'id': 2, u'title': u'list #2'}

>>> r = client.post('/api/items/reposition/5/', { 'before_id': 3 })
>>> r.status_code
200
>>> json.loads(r.content)
{u'success': True}

>>> r = client.get('/api/lists/2/items/')
>>> r.status_code
200
>>> items = json.loads(r.content)
>>> items[0]
{u'position': 0, u'id': 5, u'title': u'item #5'}
>>> items[1]
{u'position': 1, u'id': 3, u'title': u'item #3'}
>>> items[2]
{u'position': 2, u'id': 4, u'title': u'item #4'}

>>> r = client.post('/api/items/reposition/5/', { 'before_id': 1 })
>>> r.status_code
200
>>> json.loads(r.content)
{u'error': u'Cannot reposition items to other lists'}

>>> r = client.post('/api/items/move/5/', { 'destination_list_id': 1 })
>>> r.status_code
200
>>> json.loads(r.content)
{u'success': True}

>>> r = client.get('/api/lists/1/items/')
>>> r.status_code
200
>>> items = json.loads(r.content)
>>> items[0]
{u'position': 0, u'id': 1, u'title': u'item #1'}
>>> items[1]
{u'position': 1, u'id': 2, u'title': u'item #2'}
>>> items[2]
{u'position': 2, u'id': 5, u'title': u'item #5'}

# Labels
>>> r = client.post('/api/labels/', { 'title': 'label #1' })
>>> r.status_code
200
>>> json.loads(r.content)
{u'id': 1}

>>> r = client.post('/api/labels/', { 'title': 'label #2' })
>>> r.status_code
200
>>> json.loads(r.content)
{u'id': 2}

>>> r = client.post('/api/labels/', { 'title': 'label #3' })
>>> r.status_code
200
>>> json.loads(r.content)
{u'id': 3}

# /api/labels/
>>> r = client.get('/api/labels/')
>>> r.status_code
200
>>> labels = json.loads(r.content)
>>> labels[0]
{u'id': 1, u'title': u'label #1'}
>>> labels[1]
{u'id': 2, u'title': u'label #2'}
>>> labels[2]
{u'id': 3, u'title': u'label #3'}

>>> r = client.get('/api/labels/1/')
>>> r.status_code # GET /api/labels/1/
200
>>> json.loads(r.content)
{u'id': 1, u'title': u'label #1'}

>>> r = client.post('/api/labels/1/', \
{'request_method': 'PUT', 'title': 'new title'})
>>> r.status_code # POST /api/labels/1/
200
>>> json.loads(r.content)
{u'success': True}

>>> r = client.get('/api/labels/1/')
>>> r.status_code # GET /api/labels/1/
200
>>> json.loads(r.content)
{u'id': 1, u'title': u'new title'}

>>> r = client.post('/api/labels/1/', {'request_method': 'DELETE'})
>>> r.status_code # DELETE /api/labels/1/
200
>>> json.loads(r.content)
{u'success': True}

>>> r = client.get('/api/labels/1/')
>>> r.status_code
404

>>> r = client.post('/api/lists/1/labels/2/')
>>> r.status_code # POST /api/lists/1/labels/2/
200
>>> json.loads(r.content)
{u'success': True}

>>> r = client.post('/api/lists/2/labels/2/')
>>> r.status_code # POST /api/lists/2/labels/2/
200
>>> json.loads(r.content)
{u'success': True}

>>> r = client.post('/api/lists/2/labels/3/')
>>> r.status_code # POST /api/lists/2/labels/3/
200
>>> json.loads(r.content)
{u'success': True}

>>> r = client.get('/api/labels/2/lists/')
>>> r.status_code
200
>>> lists = json.loads(r.content)
>>> lists[0]['title'] # GET /api/labels/2/lists/
u"list #1"
>>> lists[1]['title'] # GET /api/labels/2/lists/
u"list #2"

>>> r = client.get('/api/lists/2/labels/')
>>> r.status_code
200
>>> labels = json.loads(r.content)
>>> labels[0]['title'] # /api/lists/2/labels/
u"label #2"
>>> labels[1]['title'] # /api/lists/2/labels/
u"label #3"

"""}
