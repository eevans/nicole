
from django.http import Http404
from models import BlogEntry
import re

flatten = lambda value: re.sub('\W', '', str(value).lower().replace(' ', '_'))

def archives_by_month():
    months = []
    result_set = BlogEntry.objects.filter(published=True).order_by('posted')
    for entry in result_set.values('posted'):
        formatted_date = entry['posted'].strftime('%B %Y')
        (year, mon) = entry['posted'].strftime('%Y %m').split()
        if not (formatted_date, (year, mon)) in months:
            months.append((formatted_date, (year, mon)))
    return months

def get_month_int(monstr):
    """
    Given a string argument containing either an abbreviated month name,
    or a numerical value, returns a valid integer for the month, or 
    raises a ValueError.
    """
    numerical = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12)
    abbreviated = ('jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug',
        'sep', 'oct', 'nov', 'dec')

    if not monstr.isdigit():
        if monstr.lower() in abbreviated:
            month = dict(zip(abbreviated, numerical))[monstr.lower()]
        else:
            raise ValueError('unable to convert %s to integer month' % monstr)
    else:
        month = int(monstr)
        if not month in numerical:
            raise ValueError('unable to convert %s to integer month' % monstr)
    return month

def get_month_int_or_404(monstr):
    """
    Given a string argument containing either an abbreviated month name,
    or a numerical value, returns a valid integer for the month, or 
    raises a django.http.Http404 exception.
    """
    try:
        return get_month_int(monstr)
    except ValueError:
        raise Http404

# vi:ai sw=4 ts=4 tw=0 et
