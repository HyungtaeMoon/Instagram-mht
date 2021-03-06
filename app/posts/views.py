import re

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect


from .models import Post, HashTag
from .forms import CommentForm, PostForm


def post_list(request):
    posts = Post.objects.all()
    context = {
        'posts': posts,
        'comment_form': CommentForm(),
    }
    return render(request, 'posts/post_list.html', context)


@login_required
def post_create(request):
    context = {}
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()

            comment_content = form.cleaned_data['comment']
            if comment_content:

                post.comments.create(
                    author=request.user,
                    content=comment_content,
                )
            return redirect('posts:post-list')
    else:
        form = PostForm()
    context['form'] = form
    return render(request, 'posts/post_create.html', context)


def comment_create(request, post_pk):
    if request.method == 'POST':
        post = Post.objects.get(pk=post_pk)
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()

            return redirect('posts:post-list')


def tag_post_list(request, tag_name):
    posts = Post.objects.filter(
        comments__tags__name=tag_name
    ).distinct()
    context = {
        'posts': posts,
    }
    return render(request, 'posts/tag_post_list.html', context)


def tag_search(request):
    search_keyword = request.GET.get('search_keyword')
    substituted_keyword = re.sub(r'#|\s+', '', search_keyword)
    return redirect('tag-post-list', substituted_keyword)
