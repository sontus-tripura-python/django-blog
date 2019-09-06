from django.shortcuts import render,get_object_or_404,redirect
from django.utils import timezone
from .forms import PostForm
from .models import Post
# Create your views here.
def post_create(request):
    posts = Post.objects.filter(publish_date__lte=timezone.now()).order_by('-publish_date')
    stuff_for_frontend = {'posts': posts}
    return render(request, 'post_create.html', stuff_for_frontend)

#create post detais
def post_views(request, pk):
    post = get_object_or_404(Post, pk=pk)
    stuff_for_frontend = { 'posts':post }
    return render (request, 'post_views.html', stuff_for_frontend)
def post_new(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.publish_date=timezone.now()
            post.save()
            return redirect('post_views', pk=post.pk)
    else:
        form = PostForm()
        stuff_for_frontend = {'form': form}
    return render(request, 'post_edit.html', stuff_for_frontend)

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
