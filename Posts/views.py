from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import PostForm
from .models import Post

# Create your views here.

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('home')
    else:
        form = PostForm()

    return render(request, 'Posts/create_post.html', {'form': form})

def post_list(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'Posts/post_list.html', {'posts': posts})

