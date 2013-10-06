from django import forms
from django.contrib import auth
from django.conf import settings
from django.core import validators
from . import models


class BootstrapInput(forms.TextInput):
    def render(self, name, value, attrs=None):
        attrs = attrs or {}
        if not attrs.get('class'):
            attrs['class'] = 'form-control'

        return super(BootstrapInput, self).render(name, value, attrs)


class BootstrapPasswordInput(BootstrapInput, forms.PasswordInput):
    pass


class EmailField(forms.EmailField):
    default_validators = forms.EmailField.default_validators + [
        validators.RegexValidator(
            regex='@%s$' % settings.AUTH_USER_EMAIL_DOMAIN,
            message='Email addresses must end at %r'
            % settings.AUTH_USER_EMAIL_DOMAIN,
        ),
    ]

    def __init__(self, domain, *args, **kwargs):
        # Simple check if we got a proper domain
        assert '.' in domain
        self.domain = domain
        super(EmailField, self).__init__(self, *args, **kwargs)

    def to_python(self, value):
        if '@' not in value:
            value = '%s@%s' % (value, self.domain)
        return value


class LoginForm(forms.Form):
    name = EmailField(
        domain=settings.AUTH_USER_EMAIL_DOMAIN,
        widget=BootstrapInput(attrs=dict(placeholder='Name')),
    )
    password = forms.CharField(widget=BootstrapPasswordInput(attrs=dict(
        placeholder='Password',
    )))

    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        email = cleaned_data.get('name', '')
        username = email.split('@')[0]
        password = cleaned_data.get('password')

        user = models.User.objects.get(email=email)
        self.user = auth.authenticate(
            username=username,
            password=password,
        )
        if user and not self.user:
            raise forms.ValidationError('Your password is incorrect.')

        pp(user)
        pp(self.user)

        if not self.user:
            self.user = models.User.objects.create_user(
                username,
                email,
                password,
            )
            self.user.is_active = False
            self.save()

        elif not self.user.is_active:
            raise forms.ValidationError('Your account is inactive, have you '
                                        'checked your mail yet?')

    def save(self, request):
        if self.user and self.user.is_active:
            auth.login(request, self.user)

        return self.user

    def clean_password(self):
        return self.cleaned_data.get('password', '').strip()

