
from django.contrib.syndication.feeds import Feed
from django.utils.feedgenerator import Atom1Feed
from django.core.urlresolvers import reverse
from models import BlogEntry

class RssFeed(Feed):
    title = 'Eric Evans\'s Weblog'
    link = property(lambda cls: reverse('index'))
    description = 'It sounded like a baby humpback whale.'

    def items(self):
        return BlogEntry.objects.filter(published=True)[:25]

class AtomFeed(RssFeed):
    feed_type = Atom1Feed
    subtitle = RssFeed.description

# vi:ai sw=4 ts=4 tw=0 et
