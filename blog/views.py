import datetime

from django.shortcuts import render
from django.http import HttpResponse
from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from django.urls import resolve

from .models import Post

# Create your views here.

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    dates_posts_made = posts.dates('created_date', 'day')
    return render(request, 'blog/post_list.html', {'posts': posts, 'dates_posts_made': dates_posts_made, 'app_name': request.resolver_match.app_name})


def post_current_time(request):
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html)


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post, 'app_name': request.resolver_match.app_name})

