from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
     path('', views.post_create, name='post_create'),
     path('post/<int:pk>/', views.post_views, name='post_views'),
     path('post/new/', views.post_new, name='post_new'),
     path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
     path('draft/', views.post_draft, name='post_draft'),
     path('post/<int:pk>/publish/', views.post_publish, name='post_publish'),
     path('accounts/login/', auth_views.LoginView.as_view(template_name="regs/login.html"), name='login'),
     #path('about/', views.about, name='about'),
    ]
