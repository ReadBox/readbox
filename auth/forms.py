from django import forms
from django.contrib import auth
from django.conf import settings
from django.core import validators

from coffin import shortcuts
from django.core import mail


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
    password = forms.CharField(
        required=False,
        widget=BootstrapPasswordInput(attrs=dict(
            placeholder='Password',
        )),
    )

    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        email = cleaned_data.get('name', '')
        username = email.split('@')[0]
        password = cleaned_data.get('password')
        if not email:
            raise forms.ValidationError('You must enter a valid email '
                                        'address')
        if not username:
            raise forms.ValidationError('Your mail address did not '
                                        'convert to a valid username.')

        users = list(
            auth.get_user_model().objects.filter(email__iexact=email)
            | auth.get_user_model().objects.filter(username__iexact=username)
        )
        if users:
            user = users[0]
        else:
            user = None

        self.user = auth.authenticate(
            username=username,
            password=password,
        )

        if user and not self.user:
            if password:
                raise forms.ValidationError('Your password is incorrect.')
            else:
                self.send_reset_mail(user)
                raise forms.ValidationError('A password reset mail has been '
                                            'sent.')

        if not self.user:
            self.user = auth.get_user_model().objects.create_user(
                username,
                email,
                password,
            )
            self.user.is_active = False
            self.user.save()
            self.send_activation_mail()

        elif not self.user.is_active:
            self.send_activation_mail()
            raise forms.ValidationError('Your account is inactive, have you '
                                        'checked your mail yet?')

        return cleaned_data

    def send_activation_mail(self):
        context = dict(
            user=self.user,
        )
        rendered_body = shortcuts.render_to_string(
            'auth/email/activation_body.txt', context)
        rendered_subjet = shortcuts.render_to_string(
            'auth/email/activation_subject.txt', context)

        mail.send_mail(
            rendered_subjet,
            rendered_body,
            settings.DEFAULT_FROM_EMAIL,
            [self.user.email],
        )

    def send_reset_mail(self, user):
        context = dict(
            user=user,
        )
        rendered_body = shortcuts.render_to_string(
            'auth/email/reset_body.txt', context)
        rendered_subjet = shortcuts.render_to_string(
            'auth/email/reset_subject.txt', context)

        mail.send_mail(
            rendered_subjet,
            rendered_body,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
        )

    def save(self, request):
        if self.user and self.user.is_active:
            auth.login(request, self.user)

        return self.user

    def clean_password(self):
        return self.cleaned_data.get('password', '').strip()


class PasswordForm(forms.Form):
    password = forms.CharField(
        required=False,
        widget=BootstrapPasswordInput(attrs=dict(
            placeholder='Password',
        )),
    )

    def save(self, request, token):
        user = token.user
        user.set_password(self.cleaned_data['password'])
        user.save()
        user = auth.authenticate(
            token=token,
        )
        if user:
            auth.login(request, user)

