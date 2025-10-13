from random import sample
from django.contrib.auth.models import User
from Posts.models import Post
from django.contrib.auth.decorators import login_required
from Accounts.models import Follower
from django.db.models import Q, Count
from django.shortcuts import render

# Create your views here.
@login_required
def home(request):
    if request.user.is_authenticated:
        # Users the current user follows
        following_users = Follower.objects.filter(follower=request.user).values_list('following', flat=True)

        # Fetch posts: public, followed, or own
        posts = Post.objects.filter(
            (Q(visibility='PUBLIC') |
             Q(author__in=following_users, visibility='FOLLOWERS') |
             Q(author=request.user)) &
            Q(author__profile__is_banned=False)
        ).order_by('-created_at').prefetch_related('react_set')

        # "People you may know" — random users excluding self and followed
        all_users = User.objects.exclude(id=request.user.id).exclude(id__in=following_users)
        people_you_may_know = sample(list(all_users), min(len(all_users), 6))
    else:
        # Anonymous users: only public posts
        posts = Post.objects.filter(visibility='PUBLIC', author__profile__is_banned=False)\
                            .order_by('-created_at').prefetch_related('react_set')
        people_you_may_know = []

    # Add reaction counts and current user's reaction (if logged in)
    for post in posts:
        reaction_counts = post.react_set.values('type').annotate(count=Count('type'))
        post.reaction_counts = {item['type']: item['count'] for item in reaction_counts}

        post.user_reacted_type = None
        if request.user.is_authenticated:
            user_reaction = post.react_set.filter(user=request.user).first()
            if user_reaction:
                post.user_reacted_type = user_reaction.type

    return render(request, 'Base/home.html', {
        'posts': posts,
        'people_you_may_know': people_you_may_know
    })
