from django.shortcuts import render
from Posts.models import Post
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def home(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'Base/home.html', {'posts': posts})