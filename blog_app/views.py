from django.shortcuts import render
from .models import Post

# from django.http import HttpResponse
# def about(request):
#     return HttpResponse('<h1> Blog about</h1>')

def home(request):
    context = {
        'posts': Post.objects.all
    }
    return render(request, 'blog_app/home.html', context)


def about(request):
    return render(request, 'blog_app/about.html', {'title': 'About'})
