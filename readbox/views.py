from django_utils import view_decorators
from django.conf import settings
from coffin import shortcuts, common
import functools
import os

from . import forms
from . import models


def path_decorator(method):
    @functools.wraps(method)
    def _path_decorator(request, path, *args, **kwargs):
        directory = shortcuts.get_object_or_404(
            models.File.objects.all().prefetch_related('tags'),
            path__iexact=path,
            path__startswith=settings.DROPBOX_BASE_PATH,
        )
        return method(request, directory, *args, **kwargs)
    return _path_decorator


@view_decorators.env
def index(request):
    return request.redirect('list', settings.DROPBOX_BASE_PATH)


@view_decorators.env
@path_decorator
def list_(request, directory):
    data = request.GET or None
    tags = directory.tags.all()
    tags_dict = dict.fromkeys(t.name for t in tags)
    form = forms.SearchForm(data)

    files = []
    if form.is_valid():
        files = directory.all_files().distinct()
        for tag in form.cleaned_data['tags']:
            files = files.filter(tags=tag)
    else:
        files = directory.children.visible()
    files = files.prefetch_related('tags')[:100]

    if request.GET:
        show_path = directory.path
    else:
        show_path = False

    if request.ajax:
        context = dict(html=dict())
        macros = common.env.get_template('readbox/macros.html')

        context['html']['main_content'] = macros.module.render_files(
            files, tags_dict=tags_dict, show_path=show_path)

        if not form.is_valid():
            context['html']['breadcrumb'] = macros.module.breadcrumb(
                directory)

        if not request.GET:
            context['tags'] = ''

        context['html']['tags'] = macros.module.tags(directory)
        context['path'] = request.get_full_path()
        context['title'] = unicode(directory)

        return context
    else:
        request.context['directory'] = directory
        request.context['files'] = files
        request.context['form'] = form
        request.context['tags'] = tags
        request.context['tags_dict'] = tags_dict
        request.context['show_path'] = show_path


@view_decorators.env
def list_simple(request, path):
    path = os.path.split(path.rstrip('/'))[0] + '/'
    directory = shortcuts.get_object_or_404(
        models.File,
        path__iexact=path,
        path__startswith=settings.DROPBOX_BASE_PATH,
    )

    files = []
    directories = []
    for child in directory.children.visible():
        if child.is_file:
            files.append((child.path, child.name))
        else:
            directories.append((child.path, child.name))

    request.context['files'] = files
    request.context['directories'] = directories


@view_decorators.env
def tags(request, tags):
    pass


@view_decorators.env
@path_decorator
def download(request, file_):
    return request.redirect(file_.get_link())


@view_decorators.env
@path_decorator
def log(request, file_):
    request.context['file'] = file_
    request.context['revisions'] = file_.revisions.all()


@view_decorators.env
def upload(request):
    pass


