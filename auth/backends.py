from django.contrib import auth


class TokenBackend(object):
    def authenticate(self, token, password):
        if token.is_valid and token.user.check_password(password):
            token.used = True
            token.save()
            return token.user

    def get_user(self, user_id):
        User = auth.get_user_model()
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return

