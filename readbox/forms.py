from django import forms
from tags_input import fields, widgets
from . import models


class SearchForm(forms.Form):
    tags = fields.TagsInputField(
        models.Tag.objects.all(),
        widget=widgets.TagsInputWidget(
            on_add_tag='updateTag',
            on_remove_tag='updateTag',
            on_change_tag='updateTag',
        ),
    )

