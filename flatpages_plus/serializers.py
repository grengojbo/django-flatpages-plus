# -*- mode: python; coding: utf-8; -*-
__author__ = 'jbo'

from rest_framework import serializers
from .models import FlatPage
# from profiles.serializers import UserSerializer
from django.contrib.auth.models import User
from rest_framework.reverse import reverse
from sorl.thumbnail.helpers import ThumbnailError
from django.conf import settings
from sorl.thumbnail import get_thumbnail
from django.template import defaultfilters
import logging

logger = logging.getLogger(__name__)

IMG_SIZE = getattr(settings, 'FP_IMG_SIZE', {'small': '260x60', 'normal': '300x300', 'big': '800'})
WORD_LIMIT = getattr(settings, 'FP_WORD_LIMIT', 45)


class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    """

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)

        # Instantiate the superclass normally
        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)

        if fields:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)


class FpUserSerializer(DynamicFieldsModelSerializer):
    """
    print UserSerializer(user)
    {'id': 2, 'username': 'jonwatts', 'email': 'jon@example.com'}

    print UserSerializer(user, fields=('id', 'email'))
    {'id': 2, 'email': 'jon@example.com'}
    """
    class Meta:
        model = User
        fields = ('id', 'username', 'email')


class FPageSerializer(DynamicFieldsModelSerializer):
    # DATE FORMAT http://docs.python.org/2/library/datetime.html#strftime-and-strptime-behavior
    # user = UserSerializer(required=False)
    # head = serializers.HyperlinkedIdentityField('images', view_name='api-image-list', lookup_field='album')
    #posts = serializers.HyperlinkedIdentityField('posts', view_name='userpost-list', lookup_field='username')
    #gender = serializers.Field('profile.gender')
    cdate = serializers.DateField(source='date_publish', format='%d/%m/%Y')
    ctiime = serializers.TimeField(source='date_publish', format='%H:%M')
    thumb = serializers.SerializerMethodField('get_image_small_src')
    image = serializers.SerializerMethodField('get_image_big_src')
    pic_thumb = serializers.SerializerMethodField('get_pic_small_src')
    pic_image = serializers.SerializerMethodField('get_pic_big_src')
    # photo = serializers.SerializerMethodField('get_photo_src')
    # photo2 = serializers.SerializerMethodField('get_photo2_src')
    detail = serializers.HyperlinkedIdentityField(view_name='api-page-detail')
    text = serializers.SerializerMethodField('get_description_txt')
    editing =serializers.SerializerMethodField('get_admin_edit')

    class Meta:
        model = FlatPage
        #fields = ('id', 'username', 'first_name', 'last_name', 'posts', )
        fields = ('id', 'title', 'category', 'content', 'photo', 'thumb', 'image', 'photo2', 'pic_thumb', 'pic_image',
                  'text', 'description', 'cdate', 'ctiime', 'detail', 'editing', 'enable_comments', 'enable_social',
                  'created', 'date_publish', 'meta_description', 'meta_keywords', 'external_url', 'owner', 'status',
                  'template_name', 'registration_required', 'sites', 'modified', 'date_unpublish', 'order', 'gonews')

    def get_admin_edit(self, obj):
        request = self.context['request']
        if request.user.is_staff:
            return reverse('admin:flatpages_plus_flatpage_change', args=[obj.pk])
        return None
    #     if not self.request.user.is_staff:
    #         return None
    #     else:
    #         return '1'

    def get_description_txt(self, obj):
        # from django.contrib.markup.templatetags.markup import markdown
        request = self.context['request']
        lim = request.QUERY_PARAMS.get('word', WORD_LIMIT)
        text = obj.content
        # if obj.description is not None:
        #     text = obj.description
        return defaultfilters.truncatewords(defaultfilters.striptags(text), int(lim))

    def get_photo_src(self, obj):
        if obj.photo is not None:
            return '{0}{1}'.format(settings.MEDIA_URL, obj.photo)
        return None

    def get_photo2_src(self, obj):
        if obj.photo2 is not None:
            return '{0}{1}'.format(settings.MEDIA_URL, obj.photo)
        return None

    def get_image_small_src(self, obj):
        request = self.context['request']
        ps = request.QUERY_PARAMS.get('photo', 'small')
        logging.debug(request.QUERY_PARAMS)
        return self.get_photo(obj.photo, rsize=IMG_SIZE.get(ps, '100x100'))

    def get_image_big_src(self, obj):
        request = self.context['request']
        ps = request.QUERY_PARAMS.get('photobig', 'big')
        return self.get_photo(obj.photo, rsize=IMG_SIZE.get(ps, '800'))

    def get_pic_small_src(self, obj):
        request = self.context['request']
        ps = request.QUERY_PARAMS.get('pic', 'normal')
        logging.debug(request.QUERY_PARAMS)
        return self.get_photo(obj.photo2, rsize=IMG_SIZE.get(ps, '100x100'))

    def get_pic_big_src(self, obj):
        request = self.context['request']
        ps = request.QUERY_PARAMS.get('picbig', 'big')
        return self.get_photo(obj.photo2, rsize=IMG_SIZE.get(ps, '800'))

    def get_photo(self, img, rsize='100x100'):
        # view = self.context['view']
        # size = int(view.kwargs['size'])
        # request = self.context['request']
        # logging.debug(request)
        try:
            return get_thumbnail(img, rsize, quality=99).url
        except IOError:
            logging.error('IOError img: {0}'.format(img))
            return None
        except ThumbnailError, ex:
            logging.error('ThumbnailError, {0} img: {1}'.format(ex.message, img))
            return None
        except ImportError:
            logging.error('ImportError img: {0}'.format(img))
            return None


class PageSerializer(DynamicFieldsModelSerializer):
    # DATE FORMAT http://docs.python.org/2/library/datetime.html#strftime-and-strptime-behavior
    # user = UserSerializer(required=False)
    # head = serializers.HyperlinkedIdentityField('images', view_name='api-image-list', lookup_field='album')
    #posts = serializers.HyperlinkedIdentityField('posts', view_name='userpost-list', lookup_field='username')
    #gender = serializers.Field('profile.gender')
    cdate = serializers.DateField(source='date_publish', format='%d/%m/%Y')
    ctiime = serializers.TimeField(source='date_publish', format='%H:%M')
    thumb = serializers.SerializerMethodField('get_image_small_src')
    image = serializers.SerializerMethodField('get_image_big_src')
    # photo = serializers.SerializerMethodField('get_photo_src')
    detail = serializers.HyperlinkedIdentityField(view_name='api-page-detail')
    text = serializers.SerializerMethodField('get_description_txt')
    editing =serializers.SerializerMethodField('get_admin_edit')

    class Meta:
        model = FlatPage
        #fields = ('id', 'username', 'first_name', 'last_name', 'posts', )
        fields = ('id', 'title', 'category', 'content', 'photo', 'thumb', 'image', 'photo2', 'text', 'description', 'cdate', 'ctiime', 'detail',
                  'editing', 'enable_comments', 'enable_social', 'created', 'date_publish', 'meta_description',
                  'meta_keywords', 'external_url')

    def get_admin_edit(self, obj):
        request = self.context['request']
        if request.user.is_staff:
            return reverse('admin:flatpages_plus_flatpage_change', args=[obj.pk])
        return None
    #     if not self.request.user.is_staff:
    #         return None
    #     else:
    #         return '1'

    def get_description_txt(self, obj):
        # from django.contrib.markup.templatetags.markup import markdown
        request = self.context['request']
        lim = request.QUERY_PARAMS.get('word', WORD_LIMIT)
        text = obj.content
        # if obj.description is not None:
        #     text = obj.description
        return defaultfilters.truncatewords(defaultfilters.striptags(text), int(lim))

    def get_image_small_src(self, obj):
        request = self.context['request']
        ps = request.QUERY_PARAMS.get('photo', 'small')
        logging.debug(request.QUERY_PARAMS)
        return self.get_photo(obj, rsize=IMG_SIZE.get(ps, '100x100'))

    def get_image_big_src(self, obj):
        request = self.context['request']
        ps = request.QUERY_PARAMS.get('photo2', 'big')
        return self.get_photo(obj, rsize=IMG_SIZE.get(ps, '800'))

    def get_photo(self, obj, rsize='100x100'):
        # view = self.context['view']
        # size = int(view.kwargs['size'])
        # request = self.context['request']
        # logging.debug(request)
        try:
            return get_thumbnail(obj.photo, rsize, quality=99).url
        except IOError:
            logging.error('IOError img: {0} url: {1}'.format(obj.id, obj.photo))
            return ''
        except ThumbnailError, ex:
            logging.error('ThumbnailError, {0} img: {1} url: {2}'.format(ex.message, obj.id, obj.photo))
            return ''
        except ImportError:
            logging.error('ImportError img: {0} url: {1}'.format(obj.id, obj.photo))
            return ''

# class ImageSerializer(serializers.ModelSerializer):
#     user = UserSerializer(required=False)
#     image_small = serializers.SerializerMethodField('get_image_small')
#     image_big = serializers.SerializerMethodField('get_image_big')
#     image_small_src = serializers.SerializerMethodField('get_image_small_src')
#     image_big_src = serializers.SerializerMethodField('get_image_big_src')
#
#     #def transform_img(self, obj, value):
#     #    return u'v='.format(value)
#     #posts = serializers.HyperlinkedIdentityField('posts', view_name='userpost-list', lookup_field='username')
#     #gender = serializers.Field('profile.gender')
#
#     class Meta:
#         model = Image
#         #fields = ('id', 'username', 'first_name', 'last_name', 'posts', )
#         fields = ('id', 'title', 'image', 'image_small', 'image_big', 'image_small_src', 'image_big_src', 'created', 'updated', 'album', 'views',
#                   'description', 'user')
#
#     def get_image_small_src(self, obj):
#         return self.get_image(obj)
#
#     def get_image_small(self, obj):
#         return u"<img src='{0}'/>".format(self.get_image(obj))
#
#     def get_image_big_src(self, obj):
#         return self.get_image(obj, rsize='big')
#
#     def get_image_big(self, obj):
#         return u"<img src='{0}'/>".format(self.get_image(obj, rsize='big'))
#
#     def get_image(self, obj, rsize='small'):
#         view = self.context['view']
#         size = int(view.kwargs['size'])
#         request = self.context['request']
#         if size in IMG_SIZE:
#             s = IMG_SIZE[size]
#         else:
#             s = IMG_SIZE_DEF
#         try:
#             return get_thumbnail(obj.image, s[rsize], quality=99).url
#         except IOError:
#             logging.error('IOError img: {0} url: {1}'.format(obj.id, obj.image))
#             return ''
#         except ThumbnailError, ex:
#             logging.error('ThumbnailError, {0} img: {1} url: {2}'.format(ex.message, obj.id, obj.image))
#             return ''
#         except ImportError:
#             logging.error('ImportError img: {0} url: {1}'.format(obj.id, obj.image))
#             return ''