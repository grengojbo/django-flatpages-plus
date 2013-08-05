# -*- mode: python; coding: utf-8; -*-
import re

from django.core.exceptions import ImproperlyConfigured

from .models import FlatPage, Categories


class FlatPageMixin(object):
    """
    Adds date_list, author_list and category_list to the context
    """

    # These attributes can be overridden in a subclass
    date_list = None
    author_list = None
    category_list = None

    def get_context_data(self, **kwargs):
        context = super(FlatPageMixin, self).get_context_data(**kwargs)
        context['date_list'] = self.get_date_list()
        context['author_list'] = self.get_author_list()
        context['category_list'] = self.get_category_list()
        try:
            context.update(self.e_context)
        except AttributeError:
            pass
        return context

    def get_date_list(self):
        if self.date_list is None:
            self.date_list = FlatPage.objects.filter(status='p').values('date_publish').cache()
        return self.date_list

    def get_author_list(self):
        if self.author_list is None:
            self.author_list = FlatPage.objects.values('owner', 'owner__username', 'owner__first_name', 'owner__last_name').order_by('owner__username').distinct().cache()
        return self.author_list

    def get_category_list(self):
        if self.category_list is None:
            self.category_list = Categories.objects.filter(is_enable=True, status='p').values('pk', 'name', 'slug',).order_by('name').distinct().cache()
        return self.category_list
