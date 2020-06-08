import math

from django.conf import settings
from django.contrib.postgres.search import SearchVector
from django.db.models import Q
from django.http import Http404, HttpRequest
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from djangoib.utils import get_ip_from_request
from . import forms, models

MAX_THREADS_PER_PAGE = getattr(settings, 'MAX_THREADS_PER_PAGE', 10)


@require_http_methods(['GET'])
def index_view(request: HttpRequest):
    boards = models.Board.objects.all()
    board_count = models.Board.objects.count()
    bucket_count = 4
    board_buckets = [None] * bucket_count
    bucket_start_cursor = 0
    elements_per_bucket = math.floor(board_count/bucket_count)
    extra_count = board_count % bucket_count
    for i in range(bucket_count):
        if bucket_start_cursor < board_count:
            taking_extra = i < extra_count
            element_count = elements_per_bucket
            if taking_extra:
                element_count += 1
            board_buckets[i] = boards[bucket_start_cursor:bucket_start_cursor+element_count]
            bucket_start_cursor += element_count
    ctx = {
        'board_buckets': board_buckets,
    }
    return render(request, 'root/index.html', ctx)


@require_http_methods(['GET', 'POST'])
def slug_view(request: HttpRequest, slug: str, page: int = 1):
    board = get_object_or_404(models.Board, slug=slug)
    thread_count = board.post_set.filter(parent=None, is_archived=False).count()
    page_count = math.ceil(thread_count / MAX_THREADS_PER_PAGE)

    if page > page_count and page > 1:
        raise Http404()

    if request.method == 'POST':
        form = forms.PostCreationForm(request.POST, request.FILES)

        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.board = board
            new_post.ip_address = get_ip_from_request(request)
            new_post.save()
            new_post_link = reverse('thread', args=(board.slug, new_post.pk,))
            return redirect('{}#p{}'.format(new_post_link, new_post.pk))
    else:
        form = forms.PostCreationForm()

    boards = models.Board.objects.all()
    thread_offset = (page-1)*MAX_THREADS_PER_PAGE
    threads = board.post_set.filter(parent=None, is_archived=False)[thread_offset:thread_offset+MAX_THREADS_PER_PAGE]
    pages = list(range(1, page_count+1))
    ctx = {
        'board': board,
        'boards': boards,
        'pages': pages,
        'page': page,
        'page_next': page_count > 1 and page < page_count,
        'page_previous': page_count > 1 and page > 1,
        'post_form': form,
        'threads': threads,
        'thread_count': thread_count,
    }
    for t in threads:
        tinfo = dict()
        tinfo['reply_count'] = t.post_set.all().count()
        tinfo['reply_with_image_count'] = t.post_set.filter(file_url__isnull=False).count()
        tinfo['expandable'] = tinfo['reply_count'] > 5
        tinfo['replies'] = t.post_set.all().order_by('-id')[:5][::-1]
        tinfo['hidden_reply_count'] = tinfo['reply_count'] - 5 if tinfo['reply_count'] > 5 else 0
        image_count = 0
        for r in tinfo['replies']:
            if r.has_image():
                image_count += 1
        if tinfo['reply_with_image_count'] > image_count:
            tinfo['hidden_reply_with_image_count'] = tinfo['reply_with_image_count'] - image_count
        else:
            tinfo['hidden_reply_with_image_count'] = 0
        setattr(t, 'ctx', tinfo)
    return render(request, 'boards/slug.html', ctx)


@require_http_methods(['GET', 'POST'])
def thread_view(request: HttpRequest, slug: str, thread_id: int):
    board = get_object_or_404(models.Board, slug=slug)
    thread = get_object_or_404(models.Post, pk=thread_id)

    print(thread.quoted_in_set.all())

    if request.method == 'POST':
        post_data = request.POST.copy()
        post_data['board'] = board.pk
        post_data['ip_address'] = get_ip_from_request(request)
        post_data['parent'] = thread.pk
        request.POST = post_data
        form = forms.ReplyCreationForm(request.POST, request.FILES)

        if form.is_valid():
            new_post = form.save()
            current_page_link = request.get_full_path()
            return redirect('{}#p{}'.format(current_page_link, new_post.pk))
    else:
        form = forms.ReplyCreationForm()

    replies = thread.post_set.all().order_by('created_at')
    reply_with_image_count = thread.post_set.filter(file_url__isnull=False).count()
    ctx = {
        'board': board,
        'boards': models.Board.objects.all(),
        'post_form': form,
        'replies': replies,
        'reply_count': len(replies),
        'reply_with_image_count': reply_with_image_count,
        'thread': thread,
    }
    return render(request, 'boards/thread.html', ctx)


@require_http_methods(['GET', 'POST'])
def catalog(request: HttpRequest, slug):
    board = get_object_or_404(models.Board, slug=slug)
    is_archive = request.resolver_match.url_name == 'archive'
    search_query = request.GET.get('q')
    if search_query:
        search_query_striped = search_query.strip()
    else:
        search_query_striped = None

    if request.method == 'POST':
        form = forms.PostCreationForm(request.POST, request.FILES)

        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.board = board
            new_post.ip_address = get_ip_from_request(request)
            new_post.save()
            new_post_link = reverse('thread', args=(board.slug, new_post.pk,))
            return redirect(new_post_link)
    else:
        form = forms.PostCreationForm()

    boards = models.Board.objects.all()
    if search_query_striped:
        threads = board.post_set.annotate(search=SearchVector('body', 'title')).filter(parent=None,
                                                                                       search=search_query_striped)
        # threads = board.post_set.filter(
        #     Q(parent=None)
        #     & Q(is_archived=is_archive)
        #     & (Q(body__contains=search_query_striped) | Q(title__contains=search_query_striped))
        # )
    else:
        threads = board.post_set.filter(parent=None, is_archived=is_archive)
    thread_count = len(threads)
    for t in threads:
        tinfo = dict()
        tinfo['reply_count'] = t.post_set.all().count()
        tinfo['reply_with_image_count'] = t.post_set.filter(file_url__isnull=False).count()
        setattr(t, 'ctx', tinfo)
    ctx = {
        'archive': is_archive,
        'board': board,
        'boards': boards,
        'catalog': not is_archive,
        'post_form': form,
        'search': search_query_striped,
        'search_query': search_query,
        'threads': threads,
        'thread_count': thread_count,
    }
    return render(request, 'boards/catalog.html', ctx)
