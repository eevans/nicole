
from os.path import dirname, join
from django.conf.urls.defaults import *
from django.contrib import admin
from feeds import RssFeed, AtomFeed
admin.autodiscover()

year_re = '?P<year>[0-9]{4}'
month_re = '?P<month>\w{3}|[0-1][0-9]'
day_re = '?P<day>[0-3][0-9]'

feeds_dict = {
    'rss2_0': RssFeed,
    'atom1_0': AtomFeed,
}

urlpatterns = patterns('',
    url(r'^$', 'nicole.views.index', name='index'),

    # Date-base (YYYY/MM/DD) hierarchy...
    url(r'^(%s)/(%s)/(%s)/(?P<name>.+)$' % (year_re, month_re, day_re),
            'nicole.views.permalink', name='perma'),
    url(r'^(%s)/(%s)/(%s)$' % (year_re, month_re, day_re), 
            'nicole.views.day_view', name='day'),
    url(r'^(%s)/(%s)/$' % (year_re, month_re), 'nicole.views.month_view',
            name='month'),
    url(r'^(%s)/$' % year_re, 'nicole.views.year_view', name='year'),

    # Post management interface
    url(r'^admin/$', 'nicole.views.post_admin', name='admin'),
    url(r'^admin/new$', 'nicole.views.create_post', name='new'),
    url(r'^admin/edit/(?P<idee>[\d]+)$', 'nicole.views.edit_post', name='edit'),
    url(r'^admin/delete/(?P<idee>[\d]+)$', 'nicole.views.delete_post',
            name='delete'),
    url(r'^admin/remove/(?P<idee>[\d]+)$', 'nicole.views.remove_post',
            name='remove'),
    url(r'^admin/save/(?P<idee>[\d]*)$', 'nicole.views.save_post', name='save'),

    # For serving static content with the devel server
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', 
        {'document_root': join(dirname(__file__), 'static')}, name='static'),

    # The django admin app
    url(r'^djadmin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^djadmin/(.*)', admin.site.root, name="djadmin"),

    # Account logins ala django.contrib.auth.views
    url(r'^accounts/login/$', 'django.contrib.auth.views.login',
            {'template_name': 'login.html'}, name='login'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout_then_login',
            name='logout'),

    # RSS and Atom feeds
    url(r'^feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed',
            {'feed_dict': feeds_dict}, name='feeds'),
)

# vi:ai sw=4 ts=4 tw=0 et
