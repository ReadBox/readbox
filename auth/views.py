from django_utils import view_decorators
from django.conf import settings

from . import forms
from . import models


@view_decorators.env
def logout(request):
    pass


@view_decorators.env
def login(request):
    form = request.context['form'] = forms.LoginForm(request.POST or None)
    if form.is_valid():
        pass

@view_decorators.env
def activate(request):
    pass
