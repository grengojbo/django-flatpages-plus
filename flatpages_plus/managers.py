# -*- mode: python; coding: utf-8; -*-
import datetime

from django.conf import settings
from django.db import models
from datetime import datetime as dt
from django.db.models import Q, F


class FlatpagesManager(models.Manager):
    """
    Allows flatpages to be listed and sorted by various criteria.
    """

    # def published(self):
    #     """Get only published"""
    #     pass

    def get_flatpages(self, sort='modified', tags=None, not_tags=None, starts_with=None,
                      owners=None, limit=None, remove=None, category=None):
        """
        The main function to return flatpages based on various criteria.
        
        This function is used by all the functions below it.
        
        All fields are optional. If nothing is passed to this manager, it will 
        return all flatpages, sorted by most recent.
        
        sort=                       What to sort the flatpages by. Optional. Default is by url.
            'created'               Returns least recently created flatpages first.
            '-created'              Returns most recently created flatpages first.
            'modified'              Returns least recently modified flatpages first.
            '-modified'             Returns most recently modified flatpages first.
            'views'                 Returns the most viewed flatpages first.
            '-views'                Returns the least viewed flatpages first.
            'random'                Returns random flatpages.
            
        tags='foo,bar,baz'          Returns all flatpages tagged with _either_      
                                    'foo', 'bar', or 'baz'. Optional.
        
        not_tags='foo,bar'          Removes any flatpages tagged with 'foo' or
                                    'bar' from the QuerySet.
                                    
        starts_with='/about/'       Return all flatpages that have a URL that 
                                    starts with '/about/'.
        
        owners=1                    Returns all flatpages by the User with ID 1. 
                                    Optional. Can be a string of IDs 
                                    (e.g. '1,5,6,8,234') or an integer 
                                    (e.g. 1). Optional.
                                    
        limit=10                    Limits the number of flatpages that are 
                                    returned to 10 results. Optional.
                                    
        remove=1                    Removes a given flatpage ID or list of IDs from
                                    the results list. Can be a string of IDs 
                                    (e.g. '1,5,6,8,234') or an integer 
                                    (e.g. 1). Optional.
        category=1                  Display only Category ID. Can be a string of IDs
                                    (e.g. '1,5,6,8,234') or an integer
                                    (e.g. 1). Optional.
        
        """
        # Get the initial queryset
        query_set = self.get_query_set()

        # Filter by the current site.
        query_set = query_set.filter((Q(date_unpublish__gte=dt.now()) | Q(date_unpublish__isnull=True)),
                                     sites__id=settings.SITE_ID, status='p')

        # Get all the filtering sort types.
        sort_types = {
            'modified': query_set.order_by('modified'),
            '-modified': query_set.order_by('-modified'),
            'created': query_set.order_by('created'),
            '-created': query_set.order_by('-created'),
            'views': query_set.order_by('-views'),
            '-views': query_set.order_by('views'),
            'random': query_set.order_by('?'),
            'date_publish': query_set.order_by('date_publish'),
            '-date_publish': query_set.order_by('-date_publish'),
            'order': query_set.order_by('order'),
            '-order': query_set.order_by('-order')
        }

        query_set = sort_types.get(sort, query_set)

        if tags is not None:
            tag_list = str(tags).split(',')
            query_set = query_set.filter(tags__name__in=tag_list).distinct()

        if not_tags is not None:
            not_tags_list = str(not_tags).split(',')
            query_set = query_set.exclude(tags__name__in=not_tags_list)

        if starts_with is not None:
            starts_with = str(starts_with)
            query_set = query_set.filter(url__startswith=starts_with)

        if owners is not None:
            owners_list = str(owners).split(',')
            query_set = query_set.filter(owner__pk__in=owners_list)

        if remove is not None:
            remove_list = str(remove).split(',')
            #query_set = query_set.exclude(pk__in=remove_list)
            query_set = query_set.exclude(category__in=remove_list)

        if category is not None:
            category_list = str(category).split(',')
            query_set = query_set.filter(category__in=category_list)

        # Limit the length of the result.
        if limit is not None:
            query_set = query_set[:int(limit)]

        return query_set.cache()




        # Try to get the type of sorting the user wants. Default to most
        # recently modified.
        # try:
        #     query_set = sort_types.get(sort, query_set)
        # except Exception, e:
        #     raise e


    def most_recently_modified(self, limit=None):
        """
        Get the most recently modified flatpages.
        """
        return self.get_flatpages(self, 'modified', limit=limit)

    def least_recently_modified(self, limit=None):
        """
        Get the least recently modified flatpages.
        """
        return self.get_flatpages(self, '-modified', limit=limit)

    def most_recently_created(self, limit=None):
        """
        Get the most recently created flatpages.
        """
        return self.get_flatpages(self, 'created', limit=limit)

    def least_recently_created(self, limit=None):
        """
        Get the least recently created flatpages.
        """
        return self.get_flatpages(self, '-created', limit=limit)

    def most_viewed(self, limit=None):
        """
        Get most viewed flatpages.
        """
        return self.get_flatpages(self, 'views', limit=limit)

    def least_viewed(self, limit=None):
        """
        Get least viewed flatpages.
        """
        return self.get_flatpages(self, '-views', limit=limit)

    def random(self, limit=None):
        """
        Get random flatpages.
        """
        return self.get_flatpages(self, 'random', limit=limit)
