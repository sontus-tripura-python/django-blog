from django.shortcuts import render
from django.utils import timezone

#from .forms import PostForm
from .models import Post
# Create your views here.
def post_create(request):
    posts = Post.objects.filter(publish_date__lte=timezone.now()).order_by('-publish_date')
    stuff_for_frontend = {'posts': posts}
    return render(request, 'post_create.html', stuff_for_frontend)
