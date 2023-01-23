from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
ListView,
DetailView,
CreateView,
UpdateView,
DeleteView
)
from .models import Post

# from django.http import HttpResponse
# def about(request):
#     return HttpResponse('<h1> Blog about</h1>')

def home(request):
    context = {
        'posts': Post.objects.all
    }
    return render(request, 'blog_app/home.html', context)


class PostListView(ListView):
    model = Post
    template_name = 'blog_app/home.html' # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog_app/post_details.html'


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']
    # template_name = 'blog_app/post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


# LoginRequiredMixin = is user logged in?
# UserPassesTestMixin = user can update only own post
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']
    # template_name = 'blog_app/post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    # can edit current logged in user
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False



class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/' #after delete going to home page
    # template_name = 'blog_app/post_confirm_delete.html'

    # can delete current logged in user
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def about(request):
    return render(request, 'blog_app/about.html', {'title': 'About'})
