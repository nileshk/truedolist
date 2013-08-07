from django.contrib import admin

from truedolist.todolists.models import TodoList, TodoItem, TodoContext, TodoLabel

admin.site.register(TodoList)
admin.site.register(TodoItem)
admin.site.register(TodoContext)
admin.site.register(TodoLabel)
