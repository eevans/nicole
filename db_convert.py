#!/usr/bin/python

import sqlite3
from nicole.models import BlogEntry
from django.contrib.auth.models import User
from tagging.models import Tag

def get_articles(dbconn):
    columns = ['id', 'title', 'name', 'created', 'posted', 'updated',
            'published', 'markdown']
    query = "SELECT %s FROM articles" % ', '.join(columns)
    cur = dbconn.cursor()
    cur.execute(query)
    for row in cur:
        yield dict(zip(columns, row))
    cur.close()

def get_tags_for_article(dbconn, idee):
    query = """
    SELECT
        tags.name
    FROM
        tags, articles_tags
    WHERE
        tags.id = articles_tags.tag_id 
    AND 
        articles_tags.article_id = ?
    """
    cur = dbconn.cursor()
    cur.execute(query, (idee,))
    tags = [i[0] for i in cur]
    cur.close()
    return tags

def get_tag_instance(name):
    try:
        tag = Tag.objects.get(name=name)
    except:
        tag = Tag(name=name)
        tag.save()
    return tag
    
def main(dbconn, djuser):
    for row in get_articles(dbconn):
        tags = get_tags_for_article(dbconn, row['id'])
        # Create the article here
        entry = BlogEntry(author=djuser, name=row['name'], title=row['title'],
            content=row['markdown'], published=row['published'])
        entry.save()
        for tag in tags:
            Tag.objects.add_tag(entry, get_tag_instance(tag))
        entry.created = row['created']
        entry.updated = row['updated']
        entry.posted = row['posted']
        entry.save()

if __name__ == '__main__':
    conn = sqlite3.connect('database.sqlite')
    user = User.objects.get(pk=1)
    main(conn, user)

# vi:ai sw=4 ts=4 tw=0 et
