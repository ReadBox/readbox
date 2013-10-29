from django.conf.urls import patterns, url

urlpatterns = patterns(
    'auth.views',
    url(r'^login/$', 'login', name='login'),
    url(r'^reset/(?P<token>\w+)/$', 'reset', name='reset'),
    url(r'^activate/(?P<token>\w+)/$', 'activate', name='activate'),
)

urlpatterns += patterns(
    '',
    url(
        r'^logout/$',
        'django.contrib.auth.views.logout',
        {'next_page': '/'},
        name='logout',
    ),
)

