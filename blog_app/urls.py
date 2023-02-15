from django.urls import path
from .views import *
from . import views


urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'),
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('about', views.about, name='blog-about'),

    path('run', views.button),
    path('discord', views.run_assistant, name='discord'),

    # path('external', views.external),
    # path('button', views.button),
    # path('output', views.output, name='output-function')
    # path('run_python_function/', views.run_python_function, name='run_python_function'),
]
