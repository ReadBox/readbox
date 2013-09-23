import models
from django.contrib import admin
from tags_input import admin as tags_input_admin


class RevisionInlineAdmin(admin.TabularInline):
    model = models.Revision
    extra = 0
    can_delete = False
    fields = readonly_fields = ('hash', 'deleted', 'created_at')


class FileAdmin(tags_input_admin.TagsInputAdmin):
    date_hierarchy = 'created_at'
    list_display = (u'id', 'path', 'hash', 'size', 'type', 'source',
                    'updated_at', 'created_at', 'deleted_at')
    list_filter = ('updated_at', 'created_at', 'deleted_at', 'type', 'source')
    raw_id_fields = ('parent',)
    search_fields = ('path',)
    inlines = [RevisionInlineAdmin]


class PermissionAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_at'
    list_display = (u'id', 'updated_at', 'created_at', 'user', 'read',
                    'rename', 'update', 'delete', 'file')
    list_filter = ('updated_at', 'created_at', 'user', 'read', 'rename',
                   'update', 'delete')
    raw_id_fields = ('file',)


class RevisionAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_at'
    list_display = (u'id', 'file', 'path', 'hash', 'deleted', 'created_at')
    list_filter = ('deleted', 'created_at')
    raw_id_fields = ('file',)
    search_fields = ('path',)


class FilePatternAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_at'
    list_display = (u'id', 'updated_at', 'created_at', 'name')
    list_filter = ('updated_at', 'created_at')
    raw_id_fields = ('patterns',)
    search_fields = ('name',)


class PatternAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_at'
    list_display = (u'id', 'updated_at', 'created_at', 'name', 'pattern',
         'example', 'child_pattern')
    list_filter = ('updated_at', 'created_at', 'child_pattern')
    search_fields = ('name',)


class TagAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_at'
    list_display = (u'id', 'updated_at', 'created_at', 'name')
    list_filter = ('updated_at', 'created_at')
    search_fields = ('name',)


class TagTypeAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_at'
    list_display = (u'id', 'updated_at', 'created_at', 'name', 'slug',
         'description', 'color')
    list_filter = ('updated_at', 'created_at')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'slug')

admin.site.register(models.File, FileAdmin)
admin.site.register(models.FilePattern, FilePatternAdmin)
admin.site.register(models.Pattern, PatternAdmin)
admin.site.register(models.Permission, PermissionAdmin)
admin.site.register(models.Revision, RevisionAdmin)
admin.site.register(models.Tag, TagAdmin)
admin.site.register(models.TagType, TagTypeAdmin)

