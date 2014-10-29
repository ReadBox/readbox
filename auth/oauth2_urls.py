from django.conf.urls import patterns, url


urlpatterns = patterns(
    'social.apps.django_app.views',
    # authentication / association
    url(r'^login/(?P<backend>[^/]+)/$', 'auth',
        name='begin'),
    url(r'^authorize/(?P<backend>[^/]+)/$', 'complete',
        name='complete'),
    # disconnection
    url(r'^disconnect/(?P<backend>[^/]+)/$', 'disconnect',
        name='disconnect'),
    url(r'^disconnect/(?P<backend>[^/]+)/(?P<association_id>[^/]+)/$',
        'disconnect', name='disconnect_individual'),
)
