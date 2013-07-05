from . import models, authentication
from django.conf import settings
from django import http
from django.core.serializers import json
from tastypie import resources, fields, authorization, serializers
from tastypie.api import Api
import json as simplejson


class PrettyJSONSerializer(serializers.Serializer):
    json_indent = 2

    def to_json(self, data, options=None):
        options = options or {}
        data = self.to_simple(data, options)
        return simplejson.dumps(data, cls=json.DjangoJSONEncoder,
                                sort_keys=True, ensure_ascii=False,
                                indent=self.json_indent)


class FileResource(resources.ModelResource):
    parent = fields.ToOneField('self', 'parent')

    def dispatch(self, request_type, request, **kwargs):
        print 'request_type: %s :: %r' % (request_type, request_type)
        #print 'request: %s :: %r' % (request, request)
        print 'kwargs: %s :: %r' % (kwargs, kwargs)

        return super(FileResource, self).dispatch(request_type, request,
                                                  **kwargs)

    def build_filters(self, filters):
        print 'filters', filters
        return super(FileResource, self).build_filters(filters)

    def prepend_urls(self):
        return [
            resources.url(
                r'^(?P<resource_name>%s)/(?P<name>.+)%s$'
                % (self._meta.resource_name, resources.trailing_slash()),
                self.wrap_view('dispatch_list'),
                name="api_get_children"),
        ]

    #def get_children(self, request, **kwargs):
    #    print 'trying to find', kwargs
    #    bundle = self.build_bundle(data={'path': kwargs['path']},
    #                               request=request)
    #    obj = self.cached_obj_get(bundle=bundle,
    #                              **self.remove_api_resource_names(kwargs))

    #    child_resource = FileResource()
    #    return child_resource.get_detail(request, parent_id=obj.pk)

    class Meta:
        queryset = models.File.objects.filter(
            path=settings.DROPBOX_BASE_PATH,
        )
        resource_name = 'file'
        detail_uri_name = 'path'
        authorization = authorization.DjangoAuthorization()
        authentication = authentication.OAuth20Authentication(
            allow_django_superuser=True)


class TopFileResource(resources.ModelResource):
    children = fields.ToManyField(FileResource, 'children')

    class Meta:
        queryset = models.File.objects.filter(
            path=settings.DROPBOX_BASE_PATH,
        )
        resource_name = 'main_file'
        detail_uri_name = 'path'
        authorization = authorization.DjangoAuthorization()
        authentication = authentication.OAuth20Authentication(
            allow_django_superuser=True)

api = Api(api_name='1.0', serializer_class=PrettyJSONSerializer)
api.register(TopFileResource())
api.register(FileResource())

