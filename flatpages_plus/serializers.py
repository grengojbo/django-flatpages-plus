# -*- mode: python; coding: utf-8; -*-
__author__ = 'jbo'

from rest_framework import serializers
from .models import FlatPage
from profiles.serializers import UserSerializer
from sorl.thumbnail import get_thumbnail
from sorl.thumbnail.helpers import ThumbnailError
from django.conf import settings
#from django.contrib.auth.models import User
import logging

logger = logging.getLogger(__name__)

IMG_SIZE = getattr(settings, 'IMAGESTORE_IMG_SIZE', {1: {'small': '260x60', 'big': '800'}})

IMG_SIZE_DEF = {'small': '260x60', 'big': '800'}


class FlatPageSerializer(serializers.ModelSerializer):
    # user = UserSerializer(required=False)
    # head = serializers.HyperlinkedIdentityField('images', view_name='api-image-list', lookup_field='album')
    #posts = serializers.HyperlinkedIdentityField('posts', view_name='userpost-list', lookup_field='username')
    #gender = serializers.Field('profile.gender')

    class Meta:
        model = FlatPage
        #fields = ('id', 'username', 'first_name', 'last_name', 'posts', )
        fields = ('id', 'title', 'category', 'content', 'photo', 'photo2', 'description')


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