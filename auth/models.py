from django.contrib.auth import models as auth_models
from django.db import models
import datetime
from django.conf import settings
import string
import random
from django.core import urlresolvers
import pytz


class ReadboxUser(auth_models.AbstractUser):
    def get_token(self):
        expires_at = settings.TOKEN_EXPIRATION_TIME + datetime.datetime.now()
        return Token.objects.create(
            user=self,
            expires_at=expires_at,
        )

    def get_activation_link(self):
        token = self.get_token()
        return '%s%s' % (
            settings.BASE_URL,
            urlresolvers.reverse('activate', kwargs=dict(token=token.token)),
        )

    def get_reset_link(self):
        token = self.get_token()
        return '%s%s' % (
            settings.BASE_URL,
            urlresolvers.reverse('reset', kwargs=dict(token=token.token)),
        )


class Token(models.Model):
    token = models.CharField(max_length=32)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    expires_at = models.DateTimeField()
    used = models.BooleanField(default=False)

    @property
    def is_valid(self):
        return not self.used and not self.is_expired

    @property
    def is_expired(self):
        now = pytz.utc.localize(datetime.datetime.utcnow())
        return now > self.expires_at

    def save(self, *args, **kwargs):
        chars = string.ascii_uppercase + string.digits
        if not self.token:
            while True:
                token = ''.join(random.choice(chars) for x in range(32))
                if not Token.objects.filter(token=token).count():
                    break

            self.token = token

        super(Token, self).save(*args, **kwargs)

    def __repr__(self):
        return '<%s[%s] %s %s>' % (
            self.__class__.__name__,
            self.token,
            self.used,
            self.expires_at,
        )

