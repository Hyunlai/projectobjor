from django.shortcuts import render
from Posts.models import Post

# Create your views here.

def home(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'Base/home.html', {'posts': posts})