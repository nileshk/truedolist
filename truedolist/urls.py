from django.conf.urls import *
from django.contrib import admin
from django.conf import settings

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'truedolist.todolists.views.home'),
    (r'^accounts/login/$', 'django.contrib.auth.views.login'),
    (r'^api/login[/]?$', 'truedolist.todolists.views.login'),    
    (r'^api/lists[/]?$', 'truedolist.todolists.views.todo_lists'),
    (r'^api/lists/(?P<todo_list_id>\d+)[/]?$', 'truedolist.todolists.views.todo_list'),
    (r'^api/lists/(?P<todo_list_id>\d+)/items[/]?$', 'truedolist.todolists.views.todo_items'),
    (r'^api/items/(?P<todo_item_id>\d+)[/]?$', 'truedolist.todolists.views.todo_item'),

    # Labels
    (r'^api/labels[/]?$', 'truedolist.todolists.views.todo_labels'),
    (r'^api/labels/(?P<label_id>\d+)[/]?$', 'truedolist.todolists.views.todo_label'),
    (r'^api/lists/(?P<todo_list_id>\d+)/labels/(?P<label_id>\d+)[/]?$',
     'truedolist.todolists.views.list_and_label'),
    (r'^api/labels/(?P<label_id>\d+)/lists[/]?$',
     'truedolist.todolists.views.todo_lists_for_label'),
    (r'^api/lists/(?P<todo_list_id>\d+)/labels[/]?$',
     'truedolist.todolists.views.todo_labels_for_list'),
    
    # Move / reposition functions
    (r'^api/lists/reposition/(?P<todo_list_id>\d+)[/]?$', 
     'truedolist.todolists.views.reposition_todo_list'), 
    (r'^api/items/reposition/(?P<todo_item_id>\d+)[/]?$', 
     'truedolist.todolists.views.reposition_todo_item'),
    (r'^api/items/move/(?P<todo_item_id>\d+)[/]?$', 
     'truedolist.todolists.views.move_todo_item'),

    # Highlight functions
    (r'^api/items/highlight/(?P<todo_item_id>\d+)/$', 
     'truedolist.todolists.views.highlight_todo_item'),
    
    # Example:
    # (r'^truedolist/', include('truedolist.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    (r'^static/(?P<path>.*)$', 'django.views.static.serve',
      {'document_root': settings.STATIC_DOC_ROOT}),

)
