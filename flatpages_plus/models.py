from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.db import models
from django.db.models import permalink
from django.utils.translation import ugettext_lazy as _

from taggit.managers import TaggableManager

from flatpages_plus.managers import FlatpagesManager


class FlatPage(models.Model):
    """
    A static page.
    """
    name = models.CharField(_('link name'), max_length=80, default=_('unamed'),
        help_text=_('The name of the page is used in creating links to \
        pages and the breadcrumbs.'))
    content = models.TextField(_('content'), blank=True)
    owner = models.ForeignKey(User, verbose_name=_('owner'), default=1,
        help_text=_('The user that is responsible for this page.'))
    views = models.IntegerField(_('views'), default=0, blank=True, null=True, 
        help_text=_('The number of the times the page has been viewed \
        (other than the owner).'), )
    tags = TaggableManager(blank=True, help_text=_('A comma seperated list of \
        tags that help to relate pages to each other.'))
    enable_comments = models.BooleanField(_('enable comments'))
    sites = models.ManyToManyField(Site, default=[settings.SITE_ID])

    
    objects = FlatpagesManager()
    
    class Meta:
        verbose_name = _('flat page')
        verbose_name_plural = _('flat pages')
        ordering = ('url',)
        
    def __unicode__(self):
        return u"%s -- %s" % (self.url, self.title)
        
    # @permalink
    # def get_absolute_url(self):
    #     return ('flatpage', None, {
    #         'url': self.url
    #     })
    
    def get_absolute_url(self): 
        return '%s' % self.url
