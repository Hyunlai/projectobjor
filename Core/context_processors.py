from django.contrib.auth.models import User
from random import sample
from Posts.models import Post  # adjust if needed
from Accounts.models import Follower  # import your follower model

def people_you_may_know(request):
    """
    Makes 'people_you_may_know' available on all templates.
    Excludes the current user and users they're already following.
    """
    if not request.user.is_authenticated:
        return {'people_you_may_know': []}

    user = request.user

    # Get all users the current user already follows
    following_users = Follower.objects.filter(follower=user).values_list('following_id', flat=True)

    # Exclude self and followed users
    all_users = User.objects.exclude(id=user.id).exclude(id__in=following_users)

    # Randomly suggest up to 6 users
    people_you_may_know = sample(list(all_users), min(len(all_users), 6)) if all_users.exists() else []

    return {'people_you_may_know': people_you_may_know}