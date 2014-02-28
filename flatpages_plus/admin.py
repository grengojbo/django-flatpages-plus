# -*- mode: python; coding: utf-8; -*-
from django.conf import settings
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
# from flatpages_plus.forms import FlatpageForm
from flatpages_plus.models import FlatPage, Categories
#from fiber.models import ContentItem
from fiber.editor import get_editor_field_name
try:
    from modeltranslation.admin import TranslationAdmin, TranslationStackedInline

    ModelAdmin = TranslationAdmin
    StackedInlineAdmin = TranslationStackedInline
except:
    ModelAdmin = admin.ModelAdmin
    StackedInlineAdmin = admin.StackedInline

#try:
#    from grappellifit.admin import TranslationAdmin, TranslationStackedInline
#    ModelAdmin = TranslationAdmin
#    StackedInlineAdmin = TranslationStackedInline
#except:
#    try:
#        from modeltranslation.admin import TranslationAdmin, TranslationStackedInline
#        ModelAdmin = TranslationAdmin
#        StackedInlineAdmin = TranslationStackedInline
#    except:
#        ModelAdmin = admin.ModelAdmin
#        StackedInlineAdmin = admin.StackedInline


class CategoriesAdmin(ModelAdmin):
    list_display = ('name', 'is_enable', 'slug', 'status',)
    list_filter = ('is_enable', 'status',)
    list_editable = ('slug', 'status',)
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)

    class Media:
        js = [
            "{0}grappelli_modeltranslation/js/tabbed_translation_fields.js".format(settings.STATIC_URL),
        ]
        css = {
            'screen': '{0}grappelli_modeltranslation/css/css/tabbed_translation_fields.css'.format(settings.STATIC_URL)}


class FlatPageAdmin(ModelAdmin):
    fieldsets = (
        (_('Title'), {
            'fields': ('title',)
        }),
        (_('Title'), {
            'fields': (('url', 'gonews', 'category'), ('date_publish', 'date_unpublish'))
        }),
        (_('Description'), {
            'classes': ('grp-collapse grp-closed',),
            'fields': ('description',)
        }),
        (_(u'Фотографии новости'), {'fields': (
            ('photo', 'photo2',),
        )}),
        (_(u'Основной текст'), {'fields': (
            get_editor_field_name('content'),
        )}),
        (_('Advanced options'), {
            'classes': ('grp-collapse grp-closed',),
            'fields': (
                ('owner', 'status',),
                'tags',
                'sites',
                ('enable_comments', 'enable_social',),
                'registration_required',
                'template_name',
                'views',
            ),
        }),
        (_('SEO'), {
            'classes': ('grp-collapse grp-closed',),
            'fields': ('meta_keywords', 'meta_description',)}),
    )
    #prepopulated_fields = {'url': ('title',)}
    list_display = ('url', 'title', 'date_publish', 'category', 'order', 'status', 'owner', 'views', 'modified',)
    list_filter = ('status', 'sites', 'enable_comments', 'registration_required', 'enable_social', 'category',)
    list_editable = ('status', 'order', )
    prepopulated_fields = {'url': ('title',)}
    search_fields = ('url', 'title', 'name', 'owner',)
    date_hierarchy = 'date_publish'
    #inlines = [NewsPhotoInline, NewsVideoInline, NewsDocumentInline]

    class Media:
        js = (
            'modeltranslation/js/force_jquery.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.24/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }


class FiberContentItemAdmin(ModelAdmin):
    group_fieldsets = True
    list_display = ('__unicode__',)
    fieldsets = (
        (None, {'fields': ('name', get_editor_field_name('content_html'))}),
    )
    date_hierarchy = 'updated'
    search_fields = ('name', 'content_html')

    class Media:
        js = (
            'modeltranslation/js/force_jquery.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.24/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }


admin.site.register(FlatPage, FlatPageAdmin)
admin.site.register(Categories, CategoriesAdmin)
# admin.site.register(ContentItem, FiberContentItemAdmin)
