from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Post

import speech_recognition as sr
import requests
import sys
from subprocess import run, PIPE
from django.http import HttpResponse
import pyttsx3
import discord

intents = discord.Intents.all()
client = discord.Client(command_prefix='!', intents=intents)

listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices)


def home(request):
    context = {
        'posts': Post.objects.all
    }
    return render(request, 'blog_app/home.html', context)


class PostListView(ListView):
    model = Post
    template_name = 'blog_app/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5


class UserPostListView(ListView):  # get specific user posts
    model = Post
    template_name = 'blog_app/user_posts.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 2

    def get_queryset(self):  # override get_queryset for specific users Post
        user = get_object_or_404(User, username=self.kwargs.get('username'))  # get username from URL
        return Post.objects.filter(author=user).order_by('-date_posted')


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
    success_url = '/'  # after delete going to home page

    # template_name = 'blog_app/post_confirm_delete.html'

    # can delete current logged in user
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def about(request):
    return render(request, 'blog_app/about.html', {'title': 'About'})


# ============================For voice to text message in Discord by discord BOT============================

def button(request):
    return render(request, 'blog_app/discord.html')


# convert my voice to virtual voice
def talk(text):
    engine.say(text)
    engine.runAndWait()


# voice command here (speak)
def take_command(request):
    with sr.Microphone() as source:
        print('listening...')
        voice = listener.listen(source)  # listener listen the user-voice by source
        user_command = listener.recognize_google(
            voice)  # by google-api, listener send audio & google back it like text
        print('user_command: ', user_command)
        talk(user_command)
        # run_assistant(user_command)

    # return render(request, 'blog_app/discord.html', {'data': user_command})
    return user_command


def run_assistant(request):
    command = take_command('')

    @client.event
    async def on_ready():
        print(f'Logged in as {client.user}')
        channel = client.get_channel(1069591088677015604)  # bot channel id
        await channel.send(command)
        talk(command)
        print(command)

    client.run("MTA2OTU1ODY0MTk2MDY5Mzg2MQ.GV8nse.mIVp19yhUzmuA_sRsfjIeOFieuO23tmv_uAUwU")  # bot Token
    return render(request, 'blog_app/discord.html', {'data': command})
    # return command

# def output(request):
#     data = requests.get('https://www.google.com/')
#     print('website data: ', data.text)
#     data = data.text
#     return render(request, 'blog_app/discord.html', {'data': data})


# main#
# def output(request):
#     data = requests.get('https://www.google.com/')
#     print('website data: ', data.text)
#     data = data.text
#     return render(request, 'blog_app/discord.html', {'data': data})
