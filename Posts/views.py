from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import PostForm, CommentForm
from .models import Post, React, Comment
from Accounts.models import Follower

# Create your views here.

# post_list does not filter follower's only posts in homepage

@login_required
def post_list(request):
    # Get a list of the users the current user is following
    following_users = Follower.objects.filter(follower=request.user).values_list('following', flat=True)

    posts = Post.objects.filter(author__in=following_users).order_by('-created_at')

    # Add reaction info to each post
    for post in posts:
        post.react_count = post.react_set.count()
        post.user_has_reacted = post.react_set.filter(user=request.user).exists()

    return render(request, 'Base/home.html', {'posts': posts})

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_list')
    else:
        form = PostForm()
    return render(request, 'Posts/create_post.html', {'form': form})

@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id, author=request.user)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = PostForm(instance=post)

    return render(request, 'Posts/edit_post.html', {'form': form, 'post': post})

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    # Checks if the logged-in user is the author of the post
    if request.user == post.author:
        post.delete()

    return redirect('home')

@login_required
def add_reaction(request, post_id, reaction_type):
    post = get_object_or_404(Post, pk=post_id)
    react_query = React.objects.filter(post=post, user=request.user, type=reaction_type)

    if react_query.exists():
        # If the user has already reacted with this type, remove the reaction
        react_query.delete()
    else:
        # If not, add the new reaction
        # This will remove any existing reactions of a different type
        # For a single reaction per user per post, you would first delete any existing reaction here
        React.objects.create(post=post, user=request.user, type=reaction_type)

    # Redirect back to the homepage
    return redirect('post_list')

@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user

            # Checks for a parent comment ID to handle replies
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