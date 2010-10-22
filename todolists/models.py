from django.db import models

from django.db import models
from django.contrib.auth.models import User
from django import forms

class TodoContext(models.Model):
    title = models.CharField(max_length=255)
#    position = models.IntegerField()
    user = models.ForeignKey(User)
    def __unicode__(self):
        return self.title

class TodoLabel(models.Model):
    """
    Model that represents TODO label

    # Initialize
    >>> User.objects.all().delete()
    >>> TodoLabel.objects.all().delete()
    >>> user1 = User.objects.create(username="TodoLabelTest", password="pw")

    # Create
    >>> label1 = TodoLabel.objects.create(title="Label1", user=user1)
    >>> label2 = TodoLabel.objects.create(title="Label2", user=user1)
    >>> label3 = TodoLabel.objects.create(title="Label3", user=user1)
    >>> list1 = TodoList.objects.create(title="List1", position=1, user=user1)
    >>> list2 = TodoList.objects.create(title="List2", position=2, user=user1)

    # Apply labels
    >>> list1.labels.add(label1)
    >>> list1.labels.add(label2)
    >>> list2.labels.add(label2)
    >>> list2.labels.add(label3)

    # Verify
    >>> TodoList.objects.filter(labels=label1)
    [<TodoList: List1>]
    >>> TodoList.objects.filter(labels=label2)
    [<TodoList: List1>, <TodoList: List2>]
    >>> TodoList.objects.filter(labels=label3)
    [<TodoList: List2>]

    >>> label1.todolist_set.all()
    [<TodoList: List1>]
    >>> label2.todolist_set.all()
    [<TodoList: List1>, <TodoList: List2>]
    >>> label3.todolist_set.all()
    [<TodoList: List2>]

    >>> list1.labels.all()
    [<TodoLabel: Label1>, <TodoLabel: Label2>]
    >>> list2.labels.all()
    [<TodoLabel: Label2>, <TodoLabel: Label3>]

    # Remove labels
    >>> list1.labels.remove(label1)
    >>> list1.labels.all()
    [<TodoLabel: Label2>]
    >>> list1.labels.remove(label2)
    >>> list1.labels.all()
    []

    # Remove lists
    >>> label3.todolist_set.remove(list2)
    >>> list2.labels.all()
    [<TodoLabel: Label2>]
    >>> label2.todolist_set.remove(list2)
    >>> list2.labels.all()
    []

    """
    title = models.CharField(max_length=255)
    user = models.ForeignKey(User)
    def __unicode__(self):
        return self.title
    
class TodoList(models.Model):
    """
    Model that represents a TODO list

    # Initialize
    >>> TodoList.objects.all().delete()
    >>> user1 = User.objects.create(username="test", password="pw")

    # Create
    >>> list1 = TodoList.objects.create(title="Work", position=1, user=user1)
    >>> list2 = TodoList.objects.create(title="Home", position=2, user=user1)

    # Verify
    >>> list1.title
    'Work'
    >>> list1.position
    1
    >>> list1.user.username
    'test'
    >>> list2.title
    'Home'
    >>> TodoList.objects.filter(title="Work")[0].title
    u'Work'
    >>> lists = TodoList.objects.filter(user=user1)
    >>> len(lists)
    2
    >>> lists[0].title
    u'Work'
    >>> lists[0].position
    1
    >>> lists[1].title
    u'Home'
    >>> lists[1].position
    2
    
    # Tear down
    >>> list1.delete()
    >>> list2.delete()
    >>> user1.delete()
    """
    title = models.CharField(max_length=255)
    position = models.IntegerField()
    user = models.ForeignKey(User)
#    todo_context = models.ForeignKey(TodoContext, null=True)
    labels = models.ManyToManyField(TodoLabel)
    def __unicode__(self):
        return self.title

class TodoItem(models.Model):
    """
    Model that represents a TODO item

    # Initialize
    >>> TodoItem.objects.all().delete()
    >>> user1 = User.objects.create(username="test2", password="pw")
    >>> list1 = TodoList.objects.create(title="NOW", position=1, user=user1)

    # Create
    >>> item1 = TodoItem.objects.create(title="item #1", position=1, \
    user=user1, todo_list=list1)
    >>> item2 = TodoItem.objects.create(title="item #2", position=2, \
    user=user1, todo_list=list1)

    # Verify
    >>> item1.title
    'item #1'
    >>> item1.position
    1
    >>> item1.todo_list.title
    'NOW'
    >>> item2.title
    'item #2'
    >>> TodoItem.objects.filter(title="item #1")[0].title
    u'item #1'
    >>> TodoItem.objects.filter(position=2)[0].title
    u'item #2'
    
    # Tear down
    >>> list1.delete()

    # List deletion should cascade to items
    >>> TodoItem.objects.filter(title="item #1")
    []
    
    """
    title = models.CharField(max_length=255)
    todo_list = models.ForeignKey(TodoList)
    position = models.IntegerField()
    user = models.ForeignKey(User)
    highlight_color = models.IntegerField(null=True)
#    todo_context = models.ForeignKey(TodoContext, null=True)
#   TODO: Highlighting    
    def __unicode__(self):
        return self.title

class TodoListForm(forms.ModelForm):
    class Meta:
        model = TodoList
        fields = ('title')
