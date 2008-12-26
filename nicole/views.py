
from django.shortcuts  import render_to_response, get_object_or_404
from django.http       import Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from datetime          import datetime
from models            import BlogEntry, Tag
from utils             import get_month_int_or_404, archives_by_month, flatten
from forms             import BlogEntryForm

# Public entries
def _render_entries(request, entries):
    user = request.user.is_authenticated() and request.user or None
    template_vars = dict(entries=entries, tags=Tag.objects.all(), 
            archives=archives_by_month(), user=user)
    return render_to_response('index.html', template_vars)

def _get_published_entries(request, year=None, month=None, day=None):
    try:
        limit = int(request.GET.get('limit'))
    except (ValueError, TypeError):
        limit = 25

    tagnames = request.GET.getlist('tag')
    filter_opts = dict(published=True)

    if tagnames:
        filter_opts['tags__in'] = Tag.objects.filter(name__in=tagnames)

    if year:
        filter_opts['posted__year'] = year
        if month: 
            filter_opts['posted__month'] = month
            if day: 
                filter_opts['posted__day'] = day

    return BlogEntry.objects.filter(**filter_opts)[:limit]

def index(request):
    entries = _get_published_entries(request)
    return _render_entries(request, entries)

def year_view(request, year):
    entries = _get_published_entries(request, year)
    return _render_entries(request, entries)

def month_view(request, year, month):
    month = get_month_int_or_404(month)
    entries = _get_published_entries(request, year, month)
    return _render_entries(request, entries)

def day_view(request, year, month, day):
    month = get_month_int_or_404(month)
    entries = _get_published_entries(request, year, month, day)
    return _render_entries(request, entries)

def permalink(request, year, month, day, name):
    month = get_month_int_or_404(month)
    entry = get_object_or_404(BlogEntry, name=name, published=True,
            posted__year=year, posted__month=month, posted__day=int(day))
    return _render_entries(request, [entry])

# Management interface
@login_required
def post_admin(request):
    drafts = BlogEntry.objects.filter(
            published=False, author=request.user).order_by('updated')
    return render_to_response('post_admin.html', {'drafts': drafts})

@login_required
def create_post(request):
    form = BlogEntryForm()
    return render_to_response('edit_post.html', {'form': form})
    
@login_required
def edit_post(request, idee):
    entry = get_object_or_404(BlogEntry, pk=idee)
    form = BlogEntryForm(dict(entry_id=entry.id, title=entry.title, 
            content=entry.content, tags=entry.tag_names))
    return render_to_response('edit_post.html', {'form': form, 'entry': entry})

@login_required
def save_post(request, idee):
    if request.method == 'POST':
        submit_names = ('save', 'publish', 'quit')
        submit = [i for i in request.POST if i in submit_names][0]
        author = request.user
        form = BlogEntryForm(request.POST)

        if form.is_valid():
            if idee:
                entry = get_object_or_404(BlogEntry, pk=idee, author=author)
                entry.title = form.cleaned_data['title']
                entry.content = form.cleaned_data['content']
            else:
                entry = BlogEntry(author=author)
                entry.title=form.cleaned_data['title']
                entry.name = flatten(entry.title) + '.html'
                entry.content = form.cleaned_data['content']
                # We need a pk before settings tag_names below
                entry.save()
            entry.tag_names = form.cleaned_data['tags']
            if submit == "publish":
                entry.published = True
                entry.posted = datetime.now()
                entry.save()
                return HttpResponseRedirect(reverse('index'))
            elif submit == "save":
                entry.save()
                return render_to_response('edit_post.html', {'form': form,
                        'entry': entry})
            else:
                entry.save()
                return HttpResponseRedirect(reverse('admin'))
        elif submit == "quit":
            return HttpResponseRedirect(reverse('admin'))
    else:
        form = BlogEntryForm()
    return render_to_response('edit_post.html', {'form': form})

@login_required
def delete_post(request, idee):
    entry = get_object_or_404(BlogEntry, pk=idee, author=request.user)
    entry.delete()
    return HttpResponseRedirect(reverse('admin'))
    
@login_required
def remove_post(request, idee):
    entry = get_object_or_404(BlogEntry, pk=idee, author=request.user)
    entry.published = False
    entry.save()
    return HttpResponseRedirect(reverse('admin'))
    
# vi:ai ts=4 sw=4 tw=0 et
