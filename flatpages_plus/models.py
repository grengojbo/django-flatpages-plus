# -*- mode: python; coding: utf-8; -*-
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.db import models
from django.db.models import permalink
from django.utils.translation import ugettext_lazy as _
from fiber.app_settings import IMAGES_DIR
from sorl.thumbnail import ImageField, get_thumbnail
from sorl.thumbnail.helpers import ThumbnailError
#from trc.models import AreaPartners
from django.contrib.sites.models import Site
import datetime

from taggit.managers import TaggableManager

from flatpages_plus.managers import FlatpagesManager

STATUS_LEVELS = (
    ('d', _('draft')),
    ('p', _('published'))
)

class PublishedFlatpagesManager(models.Manager):
    def get_query_set(self):
        now = datetime.datetime.now()
        return super(PublishedFlatpagesManager, self).get_query_set().exclude(date_unpublish__lte=now).exclude(date_publish__gte=now)

class Categories(models.Model):
    name = models.CharField(_('Name'), max_length=80, help_text=_(u'The name of the Category page'))
    slug = models.CharField(_(u"Slug"), max_length=250)
    is_enable = models.BooleanField(_(u'Enables'), default=True)
    status = models.CharField(_('status'), max_length=1, choices=STATUS_LEVELS,  default='p', help_text=_(u'Whether or not the page is visible on the site'))
    class Meta:
        verbose_name = _(u'Categorie')
        verbose_name_plural = _(u'Categories')

    def __unicode__(self):
        return u"{0}".format(self.name)

class FlatPage(models.Model):
    """
    A static page.
    """

    url = models.CharField(_('URL'), max_length=150, db_index=True)
    title = models.CharField(_('page title'), max_length=200, help_text=_(u'The title of the page is used in the HTML title of the page.'))
    name = models.CharField(_('link name'), max_length=80, default=_('unamed'), 
        help_text=_(u'The name of the page is used in creating links to pages and the breadcrumbs.'))
    category = models.ForeignKey(Categories, verbose_name=_(u'Categories'), blank=True, null=True)
    content = models.TextField(_('content'), blank=True)
    owner = models.ForeignKey(User, verbose_name=_('owner'), default=1, help_text=_(u'The user that is responsible for this page.'))
    views = models.IntegerField(_('views'), default=0, blank=True, null=True, help_text=_(u'The number of the times the page has been viewed (other than the owner).'), )
    status = models.CharField(_('status'), max_length=1, choices=STATUS_LEVELS,  default='p', help_text=_(u'Whether or not the page is visible on the site'))
    tags = TaggableManager(blank=True, help_text=_(u'A comma seperated list of tags that help to relate pages to each other.'))
    enable_comments = models.BooleanField(_('enable comments'), default=True)
    enable_social = models.BooleanField(_('enable comments'), default=True)
    template_name = models.CharField(_('template name'), max_length=70, blank=True,
        help_text=_(u"Example: 'flatpages_plus/contact_page.html'. If this isn't provided, the system will use 'flatpages/default.html'."))
    registration_required = models.BooleanField(_(u'registration required'),
        help_text=_(u"If this is checked, only logged-in users will be able to view the page."))
    sites = models.ManyToManyField(Site, default=[settings.SITE_ID])
    created = models.DateTimeField(_('created'), auto_now_add=True, 
        blank=True, null=True)
    modified = models.DateTimeField(_('modified'), auto_now=True, 
        blank=True, null=True)
    photo = ImageField(_(u'Home Photo'), upload_to=IMAGES_DIR, max_length=255, blank=True, null=True, help_text=_(u"Фото на Главной странице"))
    photo2 = ImageField(_(u'Photo'), upload_to=IMAGES_DIR, max_length=255, blank=True, null=True, help_text=_(u"Фото тексте новости"))
    date_publish = models.DateTimeField(_(u'Дата публикации'), blank=True, null=True)
    date_unpublish = models.DateTimeField(_(u'Дата отмены публикации'), blank=True, null=True)
    meta_description = models.CharField(_("Meta description"), max_length=165, blank=True, null=True)
    meta_keywords = models.CharField(_("Meta keywords"), max_length=250, blank=True, null=True)
    description = models.CharField(_(u'Description'), max_length=255, blank=True, null=True, help_text=_(u"Краткое описание выводится на главной странице"))
    order = models.IntegerField(_('Order'), default=0, help_text=_(u"Сортировать вывод новостей"))
    external_url = models.CharField(_('External URL'), max_length=150, blank=True, null=True, help_text=_(u"Ссылка на другую страницу (/catalog/marlin/) сайта или другой сайт (http://sky5.com.ua/)"))
    gonews = models.BooleanField(_(u'Перейтик к подробнее'), default=True, help_text=_(u"Если активно то при клике будет переход на страницу подробне"))
    
    objects = FlatpagesManager()
    published = PublishedFlatpagesManager()
    
    class Meta:
        verbose_name = _('flat page')
        verbose_name_plural = _('flat pages')
        ordering = ('-date_publish',)
        
    def __unicode__(self):
        return u"%s -- %s" % (self.url, self.title)
        
    # @permalink
    # def get_absolute_url(self):
    #     return ('flatpage', None, {
    #         'url': self.url
    #     })
    def save(self, *args, **kwargs):
        if self.date_publish is None:
            self.date_publish = datetime.datetime.now()
        super(FlatPage, self).save(*args, **kwargs)

    #def get_absolute_url(self):
    #    return reverse('newsly-detail', args=[self.slug])

    def get_absolute_url(self): 
        return '/%s' % self.url

    @property
    def photo_thumbnail(self):
        try:
            size = '140x140'
            im = get_thumbnail(self.photo, size, format='PNG')
            return '<img src="{url}" width="{width}" height="{height}"">'.format(url=im.url, width=im.width, height=im.height)
        except IOError:
            return u'{u}'.format(self.name)
        except ThumbnailError, ex:
            #return 'ThumbnailError, %s' % ex.message
            return u'{u}'.format(self.name)

    @property
    def photo_rss(self):
        try:
            size = '140x140'
            im = get_thumbnail(self.photo, size, format='PNG')
            #site = Site.objects.get_current()
            return im.url
            #return u"<link>http://{site}</link><title>{title}</title><url>{url}</url><height>{height}</height><width>{width}</width>".format(url=im.url, width=im.width, height=im.height, site=site.domain, title=self.title)
        except IOError:
            return u''
        except ThumbnailError, ex:
            #return 'ThumbnailError, %s' % ex.message
            return u''

    def admin_thumbnail(self):
        try:
            return '<img src="%s">' % get_thumbnail(self.photo, '100x100', format='PNG').url
        except IOError:
            return 'IOError'
        except ThumbnailError, ex:
            #return 'ThumbnailError, %s' % ex.message
            return ''

    admin_thumbnail.short_description = _('Thumbnail')
    admin_thumbnail.allow_tags = True
