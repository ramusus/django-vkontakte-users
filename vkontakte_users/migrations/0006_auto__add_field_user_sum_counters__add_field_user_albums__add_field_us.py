# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'User.sum_counters'
        db.add_column('vkontakte_users_user', 'sum_counters', self.gf('django.db.models.fields.PositiveIntegerField')(default=0), keep_default=False)

        # Adding field 'User.albums'
        db.add_column('vkontakte_users_user', 'albums', self.gf('django.db.models.fields.PositiveIntegerField')(default=0), keep_default=False)

        # Adding field 'User.audios'
        db.add_column('vkontakte_users_user', 'audios', self.gf('django.db.models.fields.PositiveIntegerField')(default=0), keep_default=False)

        # Adding field 'User.followers'
        db.add_column('vkontakte_users_user', 'followers', self.gf('django.db.models.fields.PositiveIntegerField')(default=0), keep_default=False)

        # Adding field 'User.friends'
        db.add_column('vkontakte_users_user', 'friends', self.gf('django.db.models.fields.PositiveIntegerField')(default=0), keep_default=False)

        # Adding field 'User.mutual_friends'
        db.add_column('vkontakte_users_user', 'mutual_friends', self.gf('django.db.models.fields.PositiveIntegerField')(default=0), keep_default=False)

        # Adding field 'User.notes'
        db.add_column('vkontakte_users_user', 'notes', self.gf('django.db.models.fields.PositiveIntegerField')(default=0), keep_default=False)

        # Adding field 'User.subscriptions'
        db.add_column('vkontakte_users_user', 'subscriptions', self.gf('django.db.models.fields.PositiveIntegerField')(default=0), keep_default=False)

        # Adding field 'User.user_photos'
        db.add_column('vkontakte_users_user', 'user_photos', self.gf('django.db.models.fields.PositiveIntegerField')(default=0), keep_default=False)

        # Adding field 'User.user_videos'
        db.add_column('vkontakte_users_user', 'user_videos', self.gf('django.db.models.fields.PositiveIntegerField')(default=0), keep_default=False)

        # Adding field 'User.videos'
        db.add_column('vkontakte_users_user', 'videos', self.gf('django.db.models.fields.PositiveIntegerField')(default=0), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'User.sum_counters'
        db.delete_column('vkontakte_users_user', 'sum_counters')

        # Deleting field 'User.albums'
        db.delete_column('vkontakte_users_user', 'albums')

        # Deleting field 'User.audios'
        db.delete_column('vkontakte_users_user', 'audios')

        # Deleting field 'User.followers'
        db.delete_column('vkontakte_users_user', 'followers')

        # Deleting field 'User.friends'
        db.delete_column('vkontakte_users_user', 'friends')

        # Deleting field 'User.mutual_friends'
        db.delete_column('vkontakte_users_user', 'mutual_friends')

        # Deleting field 'User.notes'
        db.delete_column('vkontakte_users_user', 'notes')

        # Deleting field 'User.subscriptions'
        db.delete_column('vkontakte_users_user', 'subscriptions')

        # Deleting field 'User.user_photos'
        db.delete_column('vkontakte_users_user', 'user_photos')

        # Deleting field 'User.user_videos'
        db.delete_column('vkontakte_users_user', 'user_videos')

        # Deleting field 'User.videos'
        db.delete_column('vkontakte_users_user', 'videos')


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
            'albums': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'audios': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'bdate': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'city': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['vkontakte_places.City']", 'null': 'True'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['vkontakte_places.Country']", 'null': 'True'}),
            'faculty': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'faculty_name': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'followers': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'friends': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'graduation': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'has_mobile': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'home_phone': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'mobile_phone': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'mutual_friends': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'notes': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'photo': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'photo_big': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'photo_medium': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'rate': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'remote_id': ('django.db.models.fields.BigIntegerField', [], {'unique': 'True'}),
            'screen_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'sex': ('django.db.models.fields.IntegerField', [], {}),
            'subscriptions': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'sum_counters': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'timezone': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'university': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'university_name': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'user_photos': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'user_videos': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'videos': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['vkontakte_users']
