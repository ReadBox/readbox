# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'TagType'
        db.create_table('readbox_tag_type', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=64)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('color', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'readbox', ['TagType'])

        # Adding unique constraint on 'TagType', fields ['slug']
        db.create_unique('readbox_tag_type', ['slug'])

        # Adding model 'Tag'
        db.create_table('readbox_tag', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
        ))
        db.send_create_signal(u'readbox', ['Tag'])

        # Adding unique constraint on 'Tag', fields ['name']
        db.create_unique('readbox_tag', ['name'])

        # Adding model 'Revision'
        db.create_table('readbox_revision', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('file', self.gf('django.db.models.fields.related.ForeignKey')(related_name='revisions', to=orm['readbox.File'])),
            ('path', self.gf('django.db.models.fields.CharField')(max_length=1024)),
            ('hash', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')()),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, blank=True)),
        ))
        db.send_create_signal(u'readbox', ['Revision'])

        # Adding unique constraint on 'Revision', fields ['path', 'hash']
        db.create_unique('readbox_revision', ['path', 'hash'])

        # Adding model 'FilePattern'
        db.create_table('readbox_file_pattern', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'readbox', ['FilePattern'])

        # Adding unique constraint on 'FilePattern', fields ['name']
        db.create_unique('readbox_file_pattern', ['name'])

        # Adding M2M table for field patterns on 'FilePattern'
        m2m_table_name = db.shorten_name('readbox_file_pattern_patterns')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('filepattern', models.ForeignKey(orm[u'readbox.filepattern'], null=False)),
            ('pattern', models.ForeignKey(orm[u'readbox.pattern'], null=False))
        ))
        db.create_unique(m2m_table_name, ['filepattern_id', 'pattern_id'])

        # Adding model 'Pattern'
        db.create_table('readbox_pattern', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('pattern', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('example', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('child_pattern', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['readbox.FilePattern'], null=True, blank=True)),
        ))
        db.send_create_signal(u'readbox', ['Pattern'])

        # Adding unique constraint on 'Pattern', fields ['name']
        db.create_unique('readbox_pattern', ['name'])

        # Adding model 'File'
        db.create_table('readbox_file', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='children', null=True, to=orm['readbox.File'])),
            ('path', self.gf('django.db.models.fields.CharField')(max_length=1024)),
            ('hash', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('size', self.gf('django.db.models.fields.IntegerField')()),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('source', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('pattern', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['readbox.FilePattern'], null=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')()),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')()),
            ('deleted_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'readbox', ['File'])

        # Adding unique constraint on 'File', fields ['path']
        db.create_unique('readbox_file', ['path'])

        # Adding M2M table for field tags on 'File'
        m2m_table_name = db.shorten_name('readbox_file_tags')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('file', models.ForeignKey(orm[u'readbox.file'], null=False)),
            ('tag', models.ForeignKey(orm[u'readbox.tag'], null=False))
        ))
        db.create_unique(m2m_table_name, ['file_id', 'tag_id'])

        # Adding model 'Permission'
        db.create_table('readbox_permission', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('read', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('rename', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('update', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('delete', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('file', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['readbox.File'])),
        ))
        db.send_create_signal(u'readbox', ['Permission'])

        # Adding unique constraint on 'Permission', fields ['user', 'file']
        db.create_unique('readbox_permission', ['user_id', 'file_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'Permission', fields ['user', 'file']
        db.delete_unique('readbox_permission', ['user_id', 'file_id'])

        # Removing unique constraint on 'File', fields ['path']
        db.delete_unique('readbox_file', ['path'])

        # Removing unique constraint on 'Pattern', fields ['name']
        db.delete_unique('readbox_pattern', ['name'])

        # Removing unique constraint on 'FilePattern', fields ['name']
        db.delete_unique('readbox_file_pattern', ['name'])

        # Removing unique constraint on 'Revision', fields ['path', 'hash']
        db.delete_unique('readbox_revision', ['path', 'hash'])

        # Removing unique constraint on 'Tag', fields ['name']
        db.delete_unique('readbox_tag', ['name'])

        # Removing unique constraint on 'TagType', fields ['slug']
        db.delete_unique('readbox_tag_type', ['slug'])

        # Deleting model 'TagType'
        db.delete_table('readbox_tag_type')

        # Deleting model 'Tag'
        db.delete_table('readbox_tag')

        # Deleting model 'Revision'
        db.delete_table('readbox_revision')

        # Deleting model 'FilePattern'
        db.delete_table('readbox_file_pattern')

        # Removing M2M table for field patterns on 'FilePattern'
        db.delete_table(db.shorten_name('readbox_file_pattern_patterns'))

        # Deleting model 'Pattern'
        db.delete_table('readbox_pattern')

        # Deleting model 'File'
        db.delete_table('readbox_file')

        # Removing M2M table for field tags on 'File'
        db.delete_table(db.shorten_name('readbox_file_tags'))

        # Deleting model 'Permission'
        db.delete_table('readbox_permission')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'readbox.file': {
            'Meta': {'unique_together': "(('path',),)", 'object_name': 'File'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {}),
            'deleted_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'hash': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': u"orm['readbox.File']"}),
            'path': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'pattern': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['readbox.FilePattern']", 'null': 'True', 'blank': 'True'}),
            'size': ('django.db.models.fields.IntegerField', [], {}),
            'source': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['readbox.Tag']", 'symmetrical': 'False'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {})
        },
        u'readbox.filepattern': {
            'Meta': {'unique_together': "(('name',),)", 'object_name': 'FilePattern', 'db_table': "'readbox_file_pattern'"},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'patterns': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['readbox.Pattern']", 'symmetrical': 'False'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'readbox.pattern': {
            'Meta': {'unique_together': "(('name',),)", 'object_name': 'Pattern'},
            'child_pattern': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['readbox.FilePattern']", 'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'example': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'pattern': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'readbox.permission': {
            'Meta': {'unique_together': "(('user', 'file'),)", 'object_name': 'Permission'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'delete': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'file': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['readbox.File']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'read': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'rename': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'update': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'readbox.revision': {
            'Meta': {'unique_together': "(('path', 'hash'),)", 'object_name': 'Revision'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'file': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'revisions'", 'to': u"orm['readbox.File']"}),
            'hash': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'path': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True', 'blank': 'True'})
        },
        u'readbox.tag': {
            'Meta': {'unique_together': "(('name',),)", 'object_name': 'Tag'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'readbox.tagtype': {
            'Meta': {'unique_together': "(('slug',),)", 'object_name': 'TagType', 'db_table': "'readbox_tag_type'"},
            'color': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '64'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['readbox']