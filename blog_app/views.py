from django.shortcuts import render

# from django.http import HttpResponse
# def about(request):
#     return HttpResponse('<h1> Blog about</h1>')

posts = [
    {
       'author': 'Maruf',
        'title': 'Blog post 01',
        'content': 'First post content',
        'date_posted': 'July 12, 2022'
    },
{
       'author': 'Eya',
        'title': 'Blog post 02',
        'content': 'Second post content',
        'date_posted': 'Aug 2, 2022'
    }
]

def home(request):
    context = {
        'posts': posts
    }
    return render(request, 'blog_app/home.html', context)


def about(request):
    return render(request, 'blog_app/about.html', {'title': 'About'})
