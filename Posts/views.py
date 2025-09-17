from django.contrib.auth.decorators import login_required
from Posts.forms import PostForm, CommentForm
from .models import Post, Comment, React
from Accounts.models import Follower, Profile
from django.db.models import Count
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.core.files.storage import default_storage
from django.contrib.auth.models import User

# Create your views here.

def search(request):
    query = request.GET.get('q')
    posts = []
    users = []

    if query:
        # Search for posts by caption
        posts = Post.objects.filter(
            Q(caption__icontains=query) | Q(author__username__icontains=query)
        ).distinct().order_by('-created_at')

        # Search for users by username
        users = User.objects.filter(
            Q(username__icontains=query)
        ).distinct()

    context = {
        'query': query,
        'posts': posts,
        'users': users
    }
    return render(request, 'Posts/search_results.html', context)

@login_required
def post_list(request):
    following_users = Follower.objects.filter(follower=request.user).values_list('following', flat=True)

    posts = Post.objects.filter(
        (Q(visibility='PUBLIC') |
         Q(author__in=following_users, visibility='FOLLOWERS') |
         Q(author=request.user)) &
        Q(author__profile__is_banned=False)
    ).order_by('-created_at').prefetch_related('react_set')

    for post in posts:
        reaction_counts = post.react_set.values('type').annotate(count=Count('type'))
        post.reaction_counts = {item['type']: item['count'] for item in reaction_counts}

        post.user_reacted_type = None
        user_reaction = post.react_set.filter(user=request.user).first()
        if user_reaction:
            post.user_reacted_type = user_reaction.type

    return render(request, 'Base/home.html', {'posts': posts})

@login_required
def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    comments = Comment.objects.filter(post=post, parent_comment=None).order_by('-created_at')

    reaction_counts = post.react_set.values('type').annotate(count=Count('type'))
    post.reaction_counts = {item['type']: item['count'] for item in reaction_counts}

    post.user_reacted_type = None
    user_reaction = post.react_set.filter(user=request.user).first()
    if user_reaction:
        post.user_reacted_type = user_reaction.type

    context = {
        'post': post,
        'comments': comments,
    }

    return render(request, 'Posts/post_detail.html', context)

@login_required
def create_post(request):
    if request.user.profile.is_banned:
        return render(request, 'Accounts/banned.html')

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
def share_post(request, post_id):
    original_post = get_object_or_404(Post, pk=post_id)

    if request.method == 'POST':
        caption = request.POST.get('caption', '')

        Post.objects.create(
            author=request.user,
            caption=caption,
            image=original_post.image if original_post.image else None,
            visibility=original_post.visibility,
            original_post=original_post
        )
        return redirect('post_list')

    return render(request, 'Posts/share_post.html', {'original_post': original_post})

@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id, author=request.user)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            if form.cleaned_data.get('clear_image'):
                if post.image:
                    if default_storage.exists(post.image.path):
                        default_storage.delete(post.image.path)
                    post.image = None

            form.save()
            return redirect('home')
    else:
        form = PostForm(instance=post)

    return render(request, 'Posts/edit_post.html', {'form': form, 'post': post})

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    if request.user == post.author:
        post.delete()

    return redirect('home')

@login_required
def add_reaction(request, post_id, reaction_type):
    post = get_object_or_404(Post, id=post_id)

    existing_reaction = React.objects.filter(user=request.user, post=post, type=reaction_type).first()

    if existing_reaction:
        existing_reaction.delete()
    else:
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
    if request.user == comment.author:
        comment.delete()
    return redirect('home')