
from django.contrib.auth.models import User
from django.db.models import Model, CharField, TextField, ForeignKey, \
        IntegerField, DateTimeField, BooleanField, ManyToManyField

class Tag(Model):
    name = CharField(max_length=32, unique=True)
    count = property(lambda s: s.blogentry_set.filter(published=True).count())

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ('name',)
        db_table = 'blog_tags'

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
    updated = DateTimeField(auto_now=True)
    published = BooleanField(default=False)
    tags = ManyToManyField(Tag)

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

    def __get_tag_names_csv(self):
        tags = self.tags.all()
        tagnames = len(tags) and ', '.join([i.name for i in tags]) or "none"
        return tagnames
    tag_names_csv = property(__get_tag_names_csv)

    def __get_tag_names(self):
        tags = self.tags.all()
        tagnames = len(tags) and ' '.join([i.name for i in tags]) or ''
        return tagnames

    # FIXME: There has got to be a cleaner way
    def __set_tag_names(self, tags_spec):
        tag_names = tags_spec.replace(',', ' ').split()
        existing_tags = self.tags.all()

        # Add any tags not already present, creating them if needed
        for tag_name in tag_names:
            if not tag_name in [i.name for i in existing_tags]:
                try:
                    new_tag = Tag.objects.get(name=tag_name)
                except Tag.DoesNotExist:
                    new_tag = Tag(name=tag_name)
                    new_tag.save()
                self.tags.add(new_tag)

        # Remove any tags not a part of the tag spec
        for tag in existing_tags:
            if not tag.name in tag_names:
                self.tags.remove(tag)
    tag_names = property(__get_tag_names, __set_tag_names)

    def __get_permalink(self):
        (year, mon, day) = self.posted.strftime('%Y %m %d').split()
        return (year, mon, day, self.name)
    permalink = property(__get_permalink)

# vi:ai sw=4 ts=4 tw=0 et
