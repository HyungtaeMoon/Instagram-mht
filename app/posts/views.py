from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

from members.models import User
from .models import Post
from .forms import PostCreateForm


def post_list(request):
    posts = Post.objects.all()
    context = {
        'posts': posts,
    }
    return render(request, 'posts/post_list.html', context)


def post_create(request):
    if request.method == 'POST':
        post = Post(
            author=User.objects.first(),
            photo=request.FILES['photo'],
        )
        post.save()
        return redirect('posts:post-list')
    else:
        form = PostCreateForm()
        context = {
            'form': form,
        }
        return render(request, 'posts/post_create.html', context)
