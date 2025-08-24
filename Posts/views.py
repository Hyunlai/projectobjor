from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import PostForm, CommentForm
from .models import Post, Comment

# Create your views here.

def post_list(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'Posts/post_list.html', {'posts': posts})

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

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    # Check if the logged-in user is the author of the post
    if request.user == post.author:
        post.delete()

    return redirect('home')


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user

            # Check for a parent comment ID to handle replies
            parent_id = request.POST.get('parent_id')
            if parent_id:
                parent_comment = get_object_or_404(Comment, pk=parent_id)
                comment.parent_comment = parent_comment

            comment.save()
            return redirect('home')
    return redirect('home')

@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)

    # Check if the logged-in user is the author of the comment
    if request.user == comment.author:
        comment.delete()

    return redirect('home')