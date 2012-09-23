# -*- mode: python; coding: utf-8; -*-
from django.conf import settings
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from flatpages_plus.forms import FlatpageForm
from flatpages_plus.models import FlatPage


class FlatPageAdmin(admin.ModelAdmin):
    form = FlatpageForm
    fieldsets = (
        (None, {'fields': (
            'url',
            'title',
            'name',
            'owner',
            'status',
            'content',
            'tags',
        )}),
        (_('Advanced options'), {
            'classes': ('collapse',), 
            'fields': (
                'sites',
                'enable_comments', 
                'registration_required', 
                'template_name',
                'views',
            )
        }),
    )
    list_display = ('url', 'title', 'name', 'status', 'owner', 'views', 'modified', 'created')
    list_filter = ('status', 'sites', 'enable_comments', 'registration_required',)
    search_fields = ('url', 'title', 'name', 'owner',)
#    class Media:
#        js = [
#            "{0}/grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js".format(settings.STATIC_ROOT),
#            "{0}/grappelli/tinymce_setup/tinymce_setup.js".format(settings.STATIC_ROOT),
#        ]

admin.site.register(FlatPage, FlatPageAdmin)
