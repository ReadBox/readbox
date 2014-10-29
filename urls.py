from django.conf.urls import patterns, include, url
from readbox import api
from django_utils import views

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    # Examples:
    # url(r'^$', 'readbox.views.home', name='home'),
    url(r'^$', 'readbox.views.index'),
    url(r'^readbox/', include('readbox.urls')),
    url(r'^auth/', include('auth.urls')),
    url(r'^api/', include(api.api.urls)),
    url(r'^tags_input/', include('tags_input.urls', namespace='tags_input')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    #url(r'^oauth2/', include('provider.oauth2.urls', namespace='oauth2')),
    url(r'^oauth2/', include('auth.oauth2_urls', namespace='social')),
    #url(r'^oauth2/', include('social.apps.django_app.urls',
    #                         namespace='social')),
)

handler400 = views.error_400
handler403 = views.error_403
handler404 = views.error_404
handler500 = views.error_500

