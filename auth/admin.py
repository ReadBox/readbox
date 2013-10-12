import models
from django.contrib import admin
from django.contrib.auth import admin as auth_admin



class ReadboxUserAdmin(auth_admin.UserAdmin):
    pass


class TokenAdmin(admin.ModelAdmin):
    list_display = (u'id', 'token', 'user', 'expires_at', 'used')
    list_filter = ('user', 'expires_at', 'used')


admin.site.register(models.ReadboxUser, ReadboxUserAdmin)
admin.site.register(models.Token, TokenAdmin)

