# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'User.bdate'
        db.add_column('vkontakte_users_user', 'bdate', self.gf('django.db.models.fields.CharField')(default='', max_length=10), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'User.bdate'
        db.delete_column('vkontakte_users_user', 'bdate')


    models = {
        'vkontakte_places.city': {
            'Meta': {'ordering': "['name']", 'object_name': 'City'},
            'area': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'cities'", 'null': 'True', 'to': "orm['vkontakte_places.Country']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'region': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'remote_id': ('django.db.models.fields.BigIntegerField', [], {'unique': 'True'})
        },
        'vkontakte_places.country': {
            'Meta': {'ordering': "['name']", 'object_name': 'Country'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'remote_id': ('django.db.models.fields.BigIntegerField', [], {'unique': 'True'})
        },
        'vkontakte_users.user': {
            'Meta': {'ordering': "['remote_id']", 'object_name': 'User'},
            'bdate': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'city': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['vkontakte_places.City']"}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['vkontakte_places.Country']"}),
            'faculty': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'faculty_name': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'graduation': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'has_mobile': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'home_phone': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'mobile_phone': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'photo': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'photo_big': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'photo_medium': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'rate': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'remote_id': ('django.db.models.fields.BigIntegerField', [], {'unique': 'True'}),
            'screen_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'sex': ('django.db.models.fields.IntegerField', [], {}),
            'timezone': ('django.db.models.fields.IntegerField', [], {}),
            'university': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'university_name': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        }
    }

    complete_apps = ['vkontakte_users']
