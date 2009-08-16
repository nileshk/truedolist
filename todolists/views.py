import logging

from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.views.generic import list_detail
from django.shortcuts import get_object_or_404, get_list_or_404, render_to_response
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.utils import simplejson
from django.template import RequestContext
from django.views.decorators.http import require_POST
from django.db import transaction

from truedolist.http_basic import logged_in_or_basicauth
from truedolist.todolists.models import TodoList, TodoItem, TodoLabel, TodoListForm

def as_json(results):
    json = simplejson.dumps(results)
    return HttpResponse(json, mimetype='application/json')

def to_json(items, map_function):
    return as_json(
        [map_function(item) for item in items])
    
def id_list(items):
    def map_function(item):
        return { 'id': item.pk,
                 'title': item.title,
                 'position': item.position }
    return to_json(items, map_function)

def success_json():
    return as_json({'success': True})

def error_json(message = True):
    return as_json({'error': message})

def labels_to_json(items):
    def map_function(item):
        return { 'id': item.pk,
                 'title': item.title }
    return to_json(items, map_function)

@require_POST
def login(request):
    logging.debug("Doing login")
    user = authenticate(username='admin', password='admin')
    logging.debug("Login successful")
    return success_json()
    
@logged_in_or_basicauth()
def todo_lists(request):
    logging.debug("todo_lists")
    # If POST, do insert
    if request.method == 'POST':
        logging.debug("request.method = POST");
        if request.POST:
            logging.debug("Post has parameters");
            title = request.POST.get('title', False)
            if title:
                logging.debug("Parameters: title = " + title)
                new_todo_list = TodoList(title=title,
                                         user=request.user,
                                         position=todo_lists_next_position(request.user))
                new_todo_list.save()
                logging.debug("List saved")
                return as_json({'id': new_todo_list.pk})
            else:
                error = 'Title cannot be empty'
        else:
            error = 'No parameters provided'
        return error_json(error)

    lists = TodoList.objects.filter(user=request.user).order_by('position')
    return id_list(lists)

def todo_lists_next_position(user):
    todo_lists = TodoList.objects.filter(user=user).order_by('-position')
    if todo_lists and len(todo_lists) > 0:
        max_todo_list = todo_lists[0]
        return int(max_todo_list.position) + 1
    return 0

def todo_items_next_position(user, todo_list):
    logging.debug("todo_items_next_position")
    todo_items = TodoItem.objects.filter(user=user, todo_list=todo_list).order_by('-position')
    if todo_items and len(todo_items) > 0:
        logging.debug("More than zero items in list")
        max_todo_item = todo_items[0]
        logging.debug("Max position is " + str(max_todo_item.position))
        return int(max_todo_item.position) + 1
    return 0

@logged_in_or_basicauth()
def todo_list(request, todo_list_id):
    # If PUT, do update
    item = get_object_or_404(TodoList, pk = todo_list_id, user = request.user)
    if is_delete(request):
        item.delete()
        return success_json()
    if is_put(request):
        title = request.POST.get('title', False)
        if title:
            item.title = title
            item.save()
            return success_json()
    # if item.todo_context:
    #     context_id = item.todo_context.pk
    # else:
    #     context_id = None
    results = {
        'id': item.pk,
        'title': item.title,
        'position': item.position,
#        'context_id': context_id,p
        }
    return as_json(results)

@logged_in_or_basicauth()
def todo_items(request, todo_list_id):
    # If POST, do insert
    if request.method == 'POST':
        logging.debug("request.method = POST");
        if request.POST:
            logging.debug("Post has parameters");
            title = request.POST.get('title', False)
            if title:
                logging.debug("Parameters: title = " + title)
                todo_list = get_object_or_404(TodoList, pk = todo_list_id,
                                              user = request.user)
                next_position = todo_items_next_position(request.user, todo_list)
                new_todo_item = TodoItem(title=title, todo_list=todo_list,
                                         user=request.user,
                                         position=next_position)
                new_todo_item.save()
                logging.debug("List saved")
                return as_json({'id': new_todo_item.pk})
            else:
                error = 'Title cannot be empty'
        else:
            error = 'No parameters provided'
        return error_json(error)

    items = TodoItem.objects.filter(user=request.user, 
                                    todo_list=todo_list_id).order_by('position')
    return id_list(items)

@logged_in_or_basicauth()
def todo_item(request, todo_item_id):
    # If POST, do insert
    # If PUT, do update
    # Else GET
    item = get_object_or_404(TodoItem, pk = todo_item_id, user = request.user)
    if is_delete(request):
        item.delete()
        return success_json()
    if is_put(request):
        title = request.POST.get('title', False)
        if title:
            item.title = title
            item.save()
            return success_json()
    # if item.todo_context:
    #     context_id = item.todo_context.pk
    # else:
    #     context_id = None
    results = {
        'id': item.pk,
        'title': item.title,
        'position': item.position,
#        'context_id': context_id,
        }
    return as_json(results)

@logged_in_or_basicauth()
def reposition_todo_item(request, todo_item_id):
    if request.method == 'POST':
        if request.POST:
            before_id = request.POST.get('before_id', False)
            if before_id:
                todo_item = get_object_or_404(TodoItem, pk = todo_item_id,
                                              user = request.user)
                todo_item_before = get_object_or_404(TodoItem, pk = before_id,
                                                     user = request.user)
                if todo_item.todo_list != todo_item_before.todo_list:
                    return as_json(
                        {'error': 'Cannot reposition items to other lists'});
                reposition_todo_item_db(todo_item, before_id, request.user)
                return success_json()
    return error_json()

@transaction.commit_on_success
def reposition_todo_item_db(todo_item, before_id, user):
    logging.debug("reposition_todo_item_db with before_id=" + str(before_id))
    logging.debug("reposition_todo_item_db todo_item.id=" + str(todo_item.id))
    todo_items = TodoItem.objects.filter(user=user, todo_list=todo_item.todo_list).order_by('position')
    position = 0
    repositioned = False
    for item in todo_items:
        logging.debug("reposition_todo_item_db, item.id=" + str(item.id))
        if item.id != todo_item.id:
            logging.debug("reposition_todo_item_db: not the item we are moving")
            if before_id != None and before_id >= 0 and int(item.id) == int(before_id):
                logging.debug("reposition_todo_item_db: moving item")
                todo_item.position = position
                todo_item.save()
                position = position + 1
                repositioned = True
            item.position = position
            item.save()
            position = position + 1
    if not repositioned:
        todo_item.position = position
        todo_item.save()

@logged_in_or_basicauth()
def reposition_todo_list(request, todo_list_id):
    if request.method == 'POST':
        if request.POST:
            before_id = request.POST.get('before_id', False)
            if before_id:
                todo_list = get_object_or_404(TodoList, pk = todo_list_id,
                                              user = request.user)
                reposition_todo_list_db(todo_list, before_id, request.user)
                return success_json()
    return error_json()

@transaction.commit_on_success
def reposition_todo_list_db(todo_list, before_id, user):
    logging.debug("reposition_todo_list_db with before_id=" + str(before_id))
    logging.debug("reposition_todo_list_db todo_list.id=" + str(todo_list.id))
    todo_lists = TodoList.objects.filter(user=user).order_by('position')
    position = 0
    repositioned = False
    for item in todo_lists:
        logging.debug("reposition_todo_list_db, list.id=" + str(item.id))
        if item.id != todo_list.id:
            logging.debug("reposition_todo_list_db: not the item we are moving")
            if before_id != None and before_id >= 0 and int(item.id) == int(before_id):
                logging.debug("reposition_todo_list_db: moving item")
                todo_list.position = position
                todo_list.save()
                position = position + 1
                repositioned = True
            item.position = position
            item.save()
            position = position + 1
    if not repositioned:
        todo_list.position = position
        todo_list.save()

@logged_in_or_basicauth()
def move_todo_item(request, todo_item_id):
    logging.debug("move_todo_item")
    if request.method != "POST" or not request.POST:
        raise Http404 # TODO This is probably the wrong error code
    todo_item = get_object_or_404(TodoItem, pk = todo_item_id, user = request.user)
    destination_list_id = request.POST.get('destination_list_id', False)
    if destination_list_id:
        logging.debug("destination_list_id:" + str(destination_list_id))
        destination_list = get_object_or_404(TodoList, pk = destination_list_id,
                                             user = request.user)
        logging.debug("destination_list.title:" + str(destination_list.title))
        todo_item.todo_list = destination_list
        logging.debug("todo_item.todo_list.title:" + str(todo_item.todo_list.title))
        todo_item.position = todo_items_next_position(request.user, destination_list)
        logging.debug("Setting position to " + str(todo_item.position))
        todo_item.save()
        return success_json()
    raise Http404 # XXX

# Create a label POST /api/labels/
# List labels GET /api/labels/
@logged_in_or_basicauth()
def todo_labels(request):
    """ GET: List labels, POST: Create a new label """
    logging.debug("todo_labels")
    if request.method == 'POST':
        logging.debug("request.method = POST");
        if request.POST:
            logging.debug("Post has parameters");
            title = request.POST.get('title', False)
            if title:
                logging.debug("Parameters: title = " + title)
                new_todo_label = TodoLabel(
                    title=title,
                    user=request.user)
                new_todo_label.save()
                logging.debug("Label saved")
                return as_json({'id': new_todo_label.pk})
            else:
                error = 'Title cannot be empty'
        else:
            error = 'No parameters provided'
        return error_json(error)

    labels = TodoLabel.objects.filter(user=request.user).order_by('title')
    return labels_to_json(labels)
    
@logged_in_or_basicauth()
def todo_label(request, label_id):
    """ Get / Update / Delete for TodoLabel """
    label = get_object_or_404(TodoLabel, pk = label_id, user = request.user)
    if is_delete(request):
        label.delete()
        return success_json()
    if is_put(request):
        title = request.POST.get('title', False)
        if title:
            label.title = title
            label.save()
            return success_json()
    results = { 'id': label.pk,
                'title': label.title }
    return as_json(results)

# Label a list POST /api/lists/:list_id/labels/:label_id/
@logged_in_or_basicauth()
def list_and_label(request, todo_list_id, label_id):
    if is_delete(request):
        todo_list = get_object_or_404(TodoList, pk = todo_list_id, 
                                      user = request.user)
        label = get_object_or_404(TodoLabel, pk = label_id,
                                  user = request.user)
        todo_list.labels.remove(label)
        return success_json()
    elif is_post(request):
        todo_list = get_object_or_404(TodoList, pk = todo_list_id, 
                                      user = request.user)
        label = get_object_or_404(TodoLabel, pk = label_id,
                                  user = request.user)
        todo_list.labels.add(label)
        return success_json()
    raise Http404 # TODO Return value indicating whether list has label

# Get lists for label /api/labels/:label_id/lists/
@logged_in_or_basicauth()
def todo_lists_for_label(request, label_id):
    label = get_object_or_404(TodoLabel, pk = label_id, user = request.user)
    return id_list(label.todolist_set.all())

# Get labels for a list /api/lists/:list_id/labels/
def todo_labels_for_list(request, todo_list_id):
    todo_list = get_object_or_404(TodoList, pk = todo_list_id,
                                  user = request.user)
    return labels_to_json(todo_list.labels.all())

def is_delete(request):
    return is_request_of_type(request, 'DELETE')

def is_put(request):
    return is_request_of_type(request, 'PUT')

def is_post(request):
    return is_request_of_type(request, 'POST')

def is_request_of_type(request, request_type):
    if request.method == request_type:
        return True
    else:
        if request.method == 'POST':
            request_method = request.POST.get('request_method', False)
            if request_method == request_type:
                return True
    return False
    
