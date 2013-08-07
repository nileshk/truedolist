
from south.db import db
from django.db import models
from truedolist.todolists.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'TodoItem'
        db.create_table('todolists_todoitem', (
            ('user', orm['todolists.TodoItem:user']),
            ('position', orm['todolists.TodoItem:position']),
            ('todo_list', orm['todolists.TodoItem:todo_list']),
            ('id', orm['todolists.TodoItem:id']),
            ('title', orm['todolists.TodoItem:title']),
        ))
        db.send_create_signal('todolists', ['TodoItem'])
        
        # Adding model 'TodoContext'
        db.create_table('todolists_todocontext', (
            ('user', orm['todolists.TodoContext:user']),
            ('id', orm['todolists.TodoContext:id']),
            ('title', orm['todolists.TodoContext:title']),
        ))
        db.send_create_signal('todolists', ['TodoContext'])
        
        # Adding model 'TodoList'
        db.create_table('todolists_todolist', (
            ('position', orm['todolists.TodoList:position']),
            ('user', orm['todolists.TodoList:user']),
            ('id', orm['todolists.TodoList:id']),
            ('title', orm['todolists.TodoList:title']),
        ))
        db.send_create_signal('todolists', ['TodoList'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'TodoItem'
        db.delete_table('todolists_todoitem')
        
        # Deleting model 'TodoContext'
        db.delete_table('todolists_todocontext')
        
        # Deleting model 'TodoList'
        db.delete_table('todolists_todolist')
        
    
    
    models = {
        'todolists.todoitem': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'position': ('django.db.models.fields.IntegerField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'todo_list': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['todolists.TodoList']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'auth.user': {
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2009, 7, 8, 22, 50, 3, 649270)'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2009, 7, 8, 22, 50, 3, 649144)'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '30', 'unique': 'True'})
        },
        'todolists.todolist': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'position': ('django.db.models.fields.IntegerField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'auth.permission': {
            'Meta': {'unique_together': "(('content_type', 'codename'),)"},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'todolists.todocontext': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'auth.group': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'unique': 'True'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True'})
        }
    }
    
    complete_apps = ['todolists']
