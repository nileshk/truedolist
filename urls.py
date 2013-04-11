from django.conf.urls.defaults import *
from django.contrib import admin
from django.conf import settings

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    (r'^api/login/$', 'todolists.views.login'),    
    (r'^api/lists/$', 'todolists.views.todo_lists'),
    (r'^api/lists/(?P<todo_list_id>\d+)/$', 'todolists.views.todo_list'),
    (r'^api/lists/(?P<todo_list_id>\d+)/items/$', 'todolists.views.todo_items'),
    (r'^api/items/(?P<todo_item_id>\d+)/$', 'todolists.views.todo_item'),

    # Labels
    (r'^api/labels/$', 'todolists.views.todo_labels'),
    (r'^api/labels/(?P<label_id>\d+)/$', 'todolists.views.todo_label'),
    (r'^api/lists/(?P<todo_list_id>\d+)/labels/(?P<label_id>\d+)/$',
     'todolists.views.list_and_label'),
    (r'^api/labels/(?P<label_id>\d+)/lists/$',
     'todolists.views.todo_lists_for_label'),
    (r'^api/lists/(?P<todo_list_id>\d+)/labels/$',
     'todolists.views.todo_labels_for_list'),
    
    # Move / reposition functions
    (r'^api/lists/reposition/(?P<todo_list_id>\d+)/$', 
     'todolists.views.reposition_todo_list'), 
    (r'^api/items/reposition/(?P<todo_item_id>\d+)/$', 
     'todolists.views.reposition_todo_item'),
    (r'^api/items/move/(?P<todo_item_id>\d+)/$', 
     'todolists.views.move_todo_item'),

    # Highlight functions
    (r'^api/items/highlight/(?P<todo_item_id>\d+)/$', 
     'todolists.views.highlight_todo_item'),
    
    # Example:
    # (r'^truedolist/', include('truedolist.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    (r'^static/(?P<path>.*)$', 'django.views.static.serve',
      {'document_root': settings.STATIC_DOC_ROOT}),

)
