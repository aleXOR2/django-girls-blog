from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from django.urls import resolve

from .models import Post, Comment
from .forms import PostForm, CommentForm

# Create your views here.

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    post_drafts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
    dates_posts_made = posts.dates('published_date', 'day')
    return render(request, 'blog/post_list.html', {'posts': posts, 'dates_posts_made': dates_posts_made, 'post_drafts': post_drafts})


def post_current_time(request):
    now = datetime.now()
    html = "<html><body>It is now %s on your PC</body></html>" % now
    return HttpResponse(html)


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})


@login_required
def post_new(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False) #as amend some non-supplied fields
            post.author = request.user
            post.created_date = timezone.now()
            if post.publish_post:
                post.published_date = timezone.now()
            post.save()
            return redirect('blog:post_detail', pk=post.pk)
    form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form, 'edit': False})


@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.updated_date = timezone.now()
            if post.publish_post:
                post.published_date = timezone.now()
            post.save()
            return redirect('blog:post_detail', pk=post.pk)
    form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form, 'edit': True})


@login_required
def post_draft_list(request):
    posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
    return render(request, 'blog/post_draft_list.html', {'posts': posts})


@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('blog:post_detail', pk=pk)


@login_required
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('blog:post_list')


@login_required
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            return redirect('blog:post_detail', pk=post.pk)
    form = CommentForm()
    return render(request, 'blog/add_comment_to_post.html', {'form': form})


@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('blog:post_detail', pk=comment.post.pk)
