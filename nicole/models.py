
from django.contrib.auth.models import User
from django.db.models import Model, CharField, TextField, ForeignKey, \
        IntegerField, DateTimeField, BooleanField
from datetime import datetime
import tagging

class BlogEntry(Model):
    MARKUP_CHOICES = (
        (1, "Markdown"),
    )

    author = ForeignKey(User)
    name = CharField(max_length=128, unique_for_date='posted')
    title = CharField(max_length=128)
    content = TextField()
    markup = IntegerField(choices=MARKUP_CHOICES, default=1)
    created = DateTimeField(auto_now_add=True)
    posted = DateTimeField(null=True, blank=True)
    updated = DateTimeField(auto_now_add=True, default=datetime.now)
    published = BooleanField(default=False)

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return self.posted.strftime('/%Y/%m/%d/') + self.name

    class Meta:
        ordering = ('-updated',)
        db_table = 'blog_entries'
        get_latest_by = 'updated'

    # These properties return formatted attributes for use in templates
    posted_datestr = property(lambda s: s.posted.strftime("%B %e, %Y"))

    def __get_created_as_string(self):
        return self.created.strftime('%B %e, %Y %H:%M')
    created_datetimestr = property(__get_created_as_string)

    def __get_updated_as_string(self):
        return self.updated.strftime('%B %e, %Y %H:%M')
    updated_datetimestr = property(__get_updated_as_string)

    def __get_permalink(self):
        (year, mon, day) = self.posted.strftime('%Y %m %d').split()
        return (year, mon, day, self.name)
    permalink = property(__get_permalink)

# XXX: http://code.google.com/p/django-tagging/issues/detail?id=128
try:
    tagging.register(BlogEntry)
except tagging.AlreadyRegistered:
    pass
    
# vi:ai sw=4 ts=4 tw=0 et
