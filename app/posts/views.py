from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect


from .models import Post
from .forms import PostCreateForm, CommentCreateForm


def post_list(request):
    posts = Post.objects.all()
    context = {
        'posts': posts,
        'comment_form': CommentCreateForm(),
    }
    return render(request, 'posts/post_list.html', context)


@login_required
def post_create(request):
    context = {}
    if request.method == 'POST':
        form = PostCreateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(author=request.user)
            return redirect('posts:post-list')
    else:
        form = PostCreateForm()
    context['form'] = form
    return render(request, 'posts/post_create.html', context)


def comment_create(request, post_pk):
    if request.method == 'POST':
        post = Post.objects.get(pk=post_pk)
        form = CommentCreateForm(request.POST)
        if form.is_valid():
            form.save(
                post=post,
                author=request.user,
            )
            return redirect('posts:post-list')
