from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib.auth.models import User
from . import models

# Create your views here.
@login_required # can only access this function if user is logged in
def create(request):
    if request.method == 'POST':
        if request.POST['title'] and request.POST['url']:
            post = models.Post()
            post.title = request.POST['title']
            if request.POST['url'].startswith('http://') or request.POST['url'].startswith('https://'):
                post.url = request.POST['url']
            else:
                post.url = 'http://' + request.POST['url']
            post.pub_date = timezone.datetime.now()
            post.author = request.user
            post.save()
            return redirect('home')
        else:
            return render(request, 'posts/create.html', {'error':'ERROR: You must include a Title and URL to create a post.'})
    else:
        return render(request, 'posts/create.html')

def home(request):
    # Get all the posts
    posts = models.Post.objects.order_by('-votes_total')
    # return the homepage, make it visible
    return render(request, 'posts/home.html', {'posts':posts})

def upvote(request, pk):
    if request.method == 'POST':
        post = models.Post.objects.get(pk=pk)
        post.votes_total += 1
        post.save()
        return redirect('home')

def downvote(request, pk):
    if request.method == 'POST':
        post = models.Post.objects.get(pk=pk)
        post.votes_total -= 1
        post.save()
        return redirect('home')

def userdetails(request, fk):
    posts = models.Post.objects.filter(author__id=fk).order_by('-votes_total')
    author = models.User.objects.get(pk=fk)
    return render(request, 'posts/userdetails.html', {'posts':posts, 'author':author})
