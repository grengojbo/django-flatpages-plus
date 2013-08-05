# -*- mode: python; coding: utf-8; -*-
from django.conf.urls import patterns, url
from flatpages_plus.views import FlatPagePlusList, FlatPagePlusDetail
#from voting.views import vote_on_object
from .models import FlatPage

urlpatterns = patterns('flatpages_plus.views',
    # url(r'^(?P<url>.*)$',
    #     view='flatpage',
    #     name='flatpage'
    # ),
    url(r'^$', FlatPagePlusList.as_view(), name='flatpage_item_list'),
    #url(r'^category/(?P<category>[\-\d\w]+)/$', FlatPagePlusList.as_view(), name='flatpage_category_list'),
    #url(r'^(?P<url>[\-\d\w]+)/$', 'flatpage', name='flatpage-detail'),
    #(r'^links/(?P<object_id>\d+)/(?P<direction>up|down|clear)vote/?$', vote_on_object, dict(model=FlatPage, template_object_name='link',
    #                        template_name='link_confirm_vote.html', allow_xmlhttprequest=True)),
    #url(r'^(?P<cat>leaser|stock|oceanplaza|news)/$', FlatPagePlusList.as_view(), name='news-category-list'),
    url(r'^(?P<slug>[\-\d\w]+)/$', FlatPagePlusDetail.as_view(), name='flatpage-detail'),
)
#urlpatterns=patterns('',
#    url(r'^page/(?P<page>[0-9]+)/$', NewsView.as_view(), name="newsly-index"),
#    url(r'^(?P<slug>[\-\d\w]+)/$', NewsDetail.as_view(), name="newsly-detail"),
#)

