from django.conf.urls import patterns, include, url
from readbox import api

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    # Examples:
    # url(r'^$', 'readbox.views.home', name='home'),
    url(r'^$', 'readbox.views.index'),
    url(r'^readbox/', include('readbox.urls')),
    url(r'^api/', include(api.api.urls)),
    url(r'^tags_input/', include('tags_input.urls', namespace='tags_input')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    url(r'^oauth2/', include('provider.oauth2.urls', namespace='oauth2')),
)

