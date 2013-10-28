import functools

from django.contrib import auth
from django_utils import view_decorators
from django.conf import settings

from . import forms
from . import models


@view_decorators.env
def login(request):
    form = request.context['form'] = forms.LoginForm(request.POST or None)
    if form.is_valid():
        form.save(request)
        if form.user.is_active:
            return request.redirect(settings.LOGIN_REDIRECT_URL)
        else:
            request.context['message'] = ('Your account has been created, '
                                          'please check your mail for the '
                                          'activation link.')
            request.context['status'] = 'success'


def _token_view(f):
    @functools.wraps(f)
    def _token_view(request, token):
        try:
            token = models.Token.objects.get(token__exact=token)
            if token.used:
                request.context['message'] = ('This token has already been '
                                              'used')
                request.context['status'] = 'primary'
            elif token.is_expired:
                request.context['message'] = ('This token has expired, please '
                                              'request a new one')
                request.context['status'] = 'danger'
            else:
                request.context['message'] = ''
                request.context['status'] = 'primary'
        except models.Token.DoesNotExist:
            token = None
            request.context['message'] = ('Unknown token, please request a '
                                          'new one')
            request.context['status'] = 'danger'

        return f(request, token)
    return _token_view


@view_decorators.env
@_token_view
def activate(request, token):
    if token and not request.context['message']:
        request.context['message'] = 'Your account has been activated'
        request.context['status'] = 'success'

        user = auth.authenticate(token=token)
        if user:
            # TODO: yes... pretty easy to activate an inactive account like
            # this, but good enough for the time being
            user.is_active = True
            user.save()
            auth.login(request, user)


@view_decorators.env
@_token_view
def reset(request, token):
    if token and not request.context['message']:
        form = forms.PasswordForm(request.POST or None)
        if form.is_valid():
            form.save(request, token)
            request.context['status'] = 'success'
            request.context['message'] = 'Your password has been reset'
        elif form.errors:
            request.context['status'] = 'danger'

        request.context['form'] = form

