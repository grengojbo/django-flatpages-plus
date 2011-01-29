import datetime

from django.db import models


class FlatpagesManager(models.Manager):
    """
    Allows flatpages to be listed and sorted by various criteria.
    """
    
    def get_flatpages(self, sort='modified', tags=None, user=None, 
                    limit=None, remove=None):
        """
        The main function to return flatpages based on various criteria.
        
        This function is used by all the functions below it.
        
        All fields are optional. If nothing is passed to this manager, it will 
        return all flatpages, sorted by most recent.
        
        sort=                       What to sort the flatpages by. Optional.
            'modified'              Returns newest flatpages first. Default.
            '-modified'             Returns oldest plug ins first.
            'created'               Returns newest flatpages first.
            '-created'              Returns oldest plug ins first.
            'views'                 Returns the most viewed flatpages first.
            '-views'                Returns the least viewed flatpages first.
            'random'                Returns random flatpages.

        tags='foo,bar,baz'          Returns all flatpages tagged with _either_      
                                    'foo', 'bar', or 'baz'. Optional.

        author=1                    Returns all flatpages by an author with ID 1. 
                                    Optional.

        limit=10                    Limits the number of flatpages that are 
                                    returned to 10 results. Optional.

        remove=1                    Removes a given plugin ID or list of IDs from
                                    the results list. Can be a string of IDs 
                                    (e.g. '1,5,6,8,234') or an integer 
                                    (e.g. 1). Optional.
        
        """
        # Get the initial queryset
        query_set = self.get_query_set()
        
        # Get all the filtering sort types.
        sort_types = {
            'modified': query_set.order_by('modified'),
            '-modified': query_set.order_by('-modified'),
            'created': query_set.order_by('created'),
            '-created': query_set.order_by('-created'),
            # TODO: Add popular filters....
            # 'popular': query_set.order_by('recent'),
            # '-popular': query_set.order_by('recent'),
            'views': query_set.order_by('-views'),
            '-views': query_set.order_by('views'),
            'random': query_set.order_by('?')
        }
        
        # Try to get the type of sorting the user wants. Default to most
        # recently modified.
        try:
            query_set = sort_types.get(sort, query_set)
        except Exception, e:
            raise e
            
        if tags:
            def get_tag_name(tag):
                """Get the name of a tag."""
                return tag.name
            tag_list = map(get_tag_name, tags)
            query_set = query_set.filter(tags__name__in=tag_list).distinct()
            
        if author:
            query_set = query_set.filter(author__pk=author)
            
        if remove:
            remove = str(remove)
            remove_list = remove.split()
            query_set = query_set.exclude(pk__in=remove_list)
            
        # Limit the length of the result.
        if limit:
            query_set = query_set[:limit]
            
        return query_set
    
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
    
    def most_popular(self, limit=None):
        """
        Get the most popular flatpages.
        """
        return self.get_flatpages(self, 'popular', limit=limit)
    
    def least_popular(self, limit=None):
        """
        Get the least popular flatpages.
        """
        return self.get_flatpages(self, '-popular', limit=limit)
    
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
