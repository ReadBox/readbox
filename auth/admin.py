import models
from django.contrib.auth import models as auth_models
from django.contrib import admin



class GroupAdmin(admin.ModelAdmin):
    list_display = (u'id', 'name')
    raw_id_fields = ('permissions',)
    search_fields = ('name',)


class PermissionAdmin(admin.ModelAdmin):
    list_display = (u'id', 'name', 'content_type', 'codename')
    search_fields = ('name',)


class ReadboxUserAdmin(admin.ModelAdmin):
    list_display = (u'id', 'password', 'last_login', 'is_superuser',
         'username', 'first_name', 'last_name', 'email', 'is_staff',
         'is_active', 'date_joined')
    list_filter = ('last_login', 'is_superuser', 'is_staff', 'is_active',
         'date_joined')
    raw_id_fields = ('groups', 'user_permissions')


class TokenAdmin(admin.ModelAdmin):
    list_display = (u'id', 'token', 'user', 'expires_at', 'used')
    list_filter = ('user', 'expires_at', 'used')



admin.site.register(auth_models.Group, GroupAdmin)
admin.site.register(auth_models.Permission, PermissionAdmin)
admin.site.register(models.ReadboxUser, ReadboxUserAdmin)
admin.site.register(models.Token, TokenAdmin)
