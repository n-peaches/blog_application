# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Post
from .forms import BlogPostForm


# Create your views here.
def post_list(request):

    posts = Post.objects.filter(published_date__lte=timezone.now()
                                ).order_by('-published_date')
    return render(request, "blog/blogposts.html", {'posts': posts})


def post_detail(request, id):

    post = get_object_or_404(Post, pk=id)
    post.views += 1 # Clock up the number of post views
    post.save()
    return render(request, "blog/postdetail.html", {'post': post})


def top_posts(request):

    posts = Post.objects.filter(published_date__lte=timezone.now()
                                ).order_by('-views')[:5]
    return render(request, "blog/blogposts.html", {'posts': posts})


def new_post(request):

    if request.method == "POST":
        form = BlogPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect(post_detail, post.pk)
    else:
        form = BlogPostForm(request.POST, request.FILES)
    return render(request, 'blog/blogpostform.html', {'form': form})


def edit_post(request, id):
    post = get_object_or_404(Post, pk=id)
    if request.method == "POST":
        form = BlogPostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect(post_detail, post.pk)
    else:
        form = BlogPostForm(instance=post)
    return render(request, 'blog/blogpostform.html', {'form': form})