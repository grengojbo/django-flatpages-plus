# -*- coding: utf-8 -*-

from modeltranslation.translator import translator, TranslationOptions
from .models import Categories, FlatPage
#from seoutils.models import Meta

class FlatPageTranslationOptions(TranslationOptions):
    fields = ('title', 'content', 'description', 'meta_description', 'meta_keywords', )


class CategoriesTranslationOptions(TranslationOptions):
    fields = ('name', )


translator.register(FlatPage, FlatPageTranslationOptions)
translator.register(Categories, CategoriesTranslationOptions)

