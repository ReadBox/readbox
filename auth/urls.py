from django.conf.urls import patterns, url

urlpatterns = patterns(
    'auth.views',
    url(r'^login/$', 'login', name='login'),
    url(r'^logout/$', 'logout', name='logout'),
    url(r'^activate/(?P<key>\w+)/$', 'activate', name='activate'),
)

