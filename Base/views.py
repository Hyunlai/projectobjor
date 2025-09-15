from django.shortcuts import render
from Posts.models import Post
from django.contrib.auth.decorators import login_required
from Accounts.models import Follower
from django.db.models import Q, Count

# Create your views here.

@login_required
def home(request):
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