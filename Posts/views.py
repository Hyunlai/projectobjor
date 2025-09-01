from django.contrib.auth.decorators import login_required
from Posts.forms import PostForm, CommentForm
from .models import Post, Comment, React
from Accounts.models import Follower
from django.db.models import Count
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.core.files.storage import default_storage


# Create your views here.

@login_required
def post_list(request):
    following_users = Follower.objects.filter(follower=request.user).values_list('following', flat=True)

    # We now filter posts from users you follow AND your own posts
    posts = Post.objects.filter(Q(author__in=following_users) | Q(author=request.user)).order_by(
        '-created_at').prefetch_related('react_set')

    for post in posts:
        # Get a count of each reaction type
        reaction_counts = post.react_set.values('type').annotate(count=Count('type'))
        post.reaction_counts = {item['type']: item['count'] for item in reaction_counts}

        # Check if the user has a reaction and get its type
        post.user_reacted_type = None
        user_reaction = post.react_set.filter(user=request.user).first()
        if user_reaction:
            post.user_reacted_type = user_reaction.type

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
            # Check if the 'clear_image' checkbox was selected
            if form.cleaned_data.get('clear_image'):
                # Check if the post already has an image
                if post.image:
                    # Delete the image file from storage
                    if default_storage.exists(post.image.path):
                        default_storage.delete(post.image.path)
                    # Set the image field to None
                    post.image = None

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
    post = get_object_or_404(Post, id=post_id)

    # We now check for an existing reaction of the specific type, which allows multiple reactions
    existing_reaction = React.objects.filter(user=request.user, post=post, type=reaction_type).first()

    if existing_reaction:
        # If the reaction already exists, delete it (unreact)
        existing_reaction.delete()
    else:
        # If the reaction doesn't exist, create it.
        React.objects.create(user=request.user, post=post, type=reaction_type)

    return redirect(request.META.get('HTTP_REFERER', 'home'))


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