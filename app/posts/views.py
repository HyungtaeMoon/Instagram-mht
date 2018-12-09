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

            p = re.compile(r'#(?P<tag>\w+)')
            tags = [HashTag.objects.get_or_create(name=name)[0]
                    for name in re.findall(p, comment.content)]
            comment.tags.set(tags)

            return redirect('posts:post-list')
