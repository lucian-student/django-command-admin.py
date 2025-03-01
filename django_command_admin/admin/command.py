from contextlib import redirect_stdout
from datetime import datetime
import io
import os

from django.conf import settings
from django.apps import apps
from django.contrib import admin
from django.core.management import call_command, get_commands
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.html import format_html
from django.urls import include, path

from ..models import Call, Command

class CommandAdmin(admin.ModelAdmin):
    list_display = ['app','name','shell','buttons',]
    list_display_links =[]
    list_filter = ['app',]
    search_fields = ['app','name']

    def filter_commands(self,commands,prefix):
        for name in commands:
            if not name.startswith(prefix):
                    continue
            yield name

    def get_queryset(self, request):
        prefix = settings.DJANGO_ADMIN_COMMANDS_PREFIX
        qs = super().get_queryset(request)
        if settings.DJANGO_ADMIN_COMMANDS_SYNC:
            for name,app in get_commands().items():
                if not name.startswith(prefix):
                    continue
                defaults = dict(app=app)
                Command.objects.get_or_create(defaults,name=name)
            Command.objects.exclude(name__in=list(self.filter_commands(get_commands().keys(),prefix))).delete()
        return qs

    def has_add_permission(self, request, obj=None):
        return settings.DJANGO_ADMIN_COMMANDS_ALLOW_ADD

    def has_change_permission(self, request, obj=None):
       return settings.DJANGO_ADMIN_COMMANDS_ALLOW_EDIT

    def has_delete_permission(self, request, obj=None):
       return settings.DJANGO_ADMIN_COMMANDS_ALLOW_DELETE

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                'django_command_admin/<slug:name>',
                self.admin_site.admin_view(self.call),
                name='django_command_admin_call',
            )
        ]
        return custom_urls + urls

    def shell(self, command):
        return format_html('<code>python manage.py %s</code>' % command.name)
    shell.short_description = 'shell'
    shell.allow_tags = True

    def buttons(self, command):
        return format_html(
            '<a class="button" href="{}" target="_blank">Run</a> ',
            reverse('admin:django_command_admin_call', args=[command.name]),
        )
    buttons.short_description = ''
    buttons.allow_tags = True

    def call(self, request, name):
        started_at = datetime.now()
        with io.StringIO() as buf, redirect_stdout(buf):
            result = call_command(name)
            stdout = buf.getvalue()
        obj = Call.objects.create(
            app=get_commands()[name],
            name=name,
            stdout=stdout,
            started_at=started_at,
            finished_at=datetime.now()
        )
        url = reverse('admin:django_command_admin_call_change',args=[obj.pk])
        return redirect(url)
