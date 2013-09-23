from django_utils.management.commands import base_command
from django.conf import settings
import re
from readbox import models

class Command(base_command.CustomBaseCommand):
    loggers = base_command.CustomBaseCommand.loggers + (
        'readbox.dropbox',
    )

    def handle(self, *args, **kwargs):
        base_command.CustomBaseCommand.handle(self, *args, **kwargs)

        self.tag_types = dict(
            (t.name, t) for t in
            models.TagType.objects.all()
        )

        self.handle_main_directory()

    def get_tag(self, tags, type_, name):
        tag = tags.get(name)
        if not tag:
            tag = tags[name] = models.Tag.objects.create(
                type=type_,
                name=name,
            )
        return tag

    def get_tag_type(self, name):
        if name not in self.tag_types:
            self.tag_types[name] = models.TagType.objects.create(name=name)
        return self.tag_types[name]

    def add_recursive(self, tag, directory):
        tag.files.add(*models.File.objects.filter(
            path__istartswith=directory.path))

    def handle_main_directory(self):
        main = models.File.objects.get(path=settings.DROPBOX_BASE_PATH)

        tag_type = self.get_tag_type('Year')
        tags = dict((t.name, t) for t in tag_type.tags.all())
        for directory in main.children.all_directories():
            match = re.search('\(([a-zA-Z]+ jaar)\)', directory.name)
            if match:
                tag = self.get_tag(tags, tag_type, match.group(1))
                print 'Processing year %r: %s' % (directory, directory.path)
                self.add_recursive(tag, directory)
                self.handle_year_directory(directory)

    def handle_year_directory(self, year):
        code_type = self.get_tag_type('Class Code')
        name_type = self.get_tag_type('Class Name')
        quarter_type = self.get_tag_type('Quarter')
        code_tags = dict((t.name, t) for t in code_type.tags.all())
        name_tags = dict((t.name, t) for t in name_type.tags.all())
        quarter_tags = dict((t.name, t) for t in quarter_type.tags.all())

        for directory in year.children.all_directories():
            match = re.match(
                '(?P<name>[a-zA-Z0-9& -]+)'
                '\((?P<code>[A-Z0-9 -]+)\)'
                '( *(?P<quarter>Q[0-9]*))?',
                directory.name,
            )
            if match:
                print 'Processing subject: %r: %s' % (
                    directory, directory.path)

                tag = self.get_tag(code_tags, code_type, match.group('code'))
                self.add_recursive(tag, directory)
                tag = self.get_tag(name_tags, name_type, match.group('name'))
                self.add_recursive(tag, directory)

                quarter = match.group('quarter')
                if quarter:
                    tag = self.get_tag(quarter_tags, quarter_type, quarter)
                self.add_recursive(tag, directory)

