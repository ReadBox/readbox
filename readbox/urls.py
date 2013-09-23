from django.conf.urls import patterns, url

urlpatterns = patterns(
    'readbox.views',
    url(r'^$', 'index', name='index'),
    url(r'^upload/$', 'upload', name='upload'),
    url(r'^log(?P<path>/.*)/$', 'log', name='log'),
    url(r'^download(?P<path>/.*)/$', 'download', name='download'),
    url(r'^list(?P<path>/.*/)$', 'list_', name='list'),
    url(r'^list_simple(?P<path>/.*/)$', 'list_simple', name='list_simple'),
    url(r'^tags(?P<path>/.*/)$', 'tags', name='tags'),
)

