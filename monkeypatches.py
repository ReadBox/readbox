def patch():
    '''Monkeypatch Django to mimic Jinja2 behaviour'''
    from django.utils import safestring
    if not hasattr(safestring, '__html__'):
        safestring.SafeString.__html__ = lambda self: str(self)
        safestring.SafeUnicode.__html__ = lambda self: unicode(self)

