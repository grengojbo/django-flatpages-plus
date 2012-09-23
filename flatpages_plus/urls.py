from django.conf.urls import patterns

urlpatterns = patterns('flatpages_plus.views',
    # url(r'^(?P<url>.*)$',
    #     view='flatpage',
    #     name='flatpage'
    # ),
    (r'^(?P<url>.*)$', 'flatpage'),
)
