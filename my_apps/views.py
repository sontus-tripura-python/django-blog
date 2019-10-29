from django.contrib.auth.decorators import login_required
from django.shortcuts import render,get_object_or_404,redirect
from django.utils import timezone
from .forms import PostForm, CommentForm, Comment
from .models import Post
# Create your views here.
def about(request):
    return render(request, 'about.html')

def post_create(request):
    posts = Post.objects.filter(publish_date__lte=timezone.now()).order_by('-publish_date')
    stuff_for_frontend = {'posts': posts}
    return render(request, 'post_create.html', stuff_for_frontend)

#create post detais
def post_views(request, pk):
    post = get_object_or_404(Post, pk=pk)
    stuff_for_frontend = { 'posts':post }
    return render (request, 'post_views.html', stuff_for_frontend)

@login_required
def post_new(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_views', pk=post.pk)
    else:
        form = PostForm()
        stuff_for_frontend = {'form': form}
    return render(request, 'post_edit.html', stuff_for_frontend)

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':

        # updating an existing form
        form = PostForm(request.POST, instance=post)

        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user

            post.save()
            return redirect('post_views', pk=post.pk)
    else:
        form = PostForm(instance=post)
        stuff_for_frontend = {'form': form}
    return render(request, 'post_edit.html', stuff_for_frontend)

@login_required
def post_draft(request):
    posts = Post.objects.filter(publish_date__isnull=True).order_by('-created_date')
    stuff_for_frontend = {'posts': posts }
    return render(request, 'post_draft.html',  stuff_for_frontend)

@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_views', pk=pk)

def logout(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("main:homepage")

def add_comment_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            return redirect('post_views', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'add_comment_post.html', {'form': form })


def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('post_views', pk=comment.post.pk)

def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_views', pk=comment.post.pk)
