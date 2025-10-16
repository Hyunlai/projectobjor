from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .forms import UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from Posts.models import Post, React
from django.db.models import Count, Q
from .models import Profile, Follower
from Admin.models import Admin
from django.contrib.auth.models import User
# Create your views here.

def lighten_color(hex_color, factor=0.2, max_light=220):
    hex_color = hex_color.lstrip('#')
    rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    lightened = tuple(min(int(c + (255 - c) * factor), max_light) for c in rgb)
    return '#' + ''.join(f'{c:02x}' for c in lightened)

def darken_color(hex_color, factor=0.2, min_dark=30):
    hex_color = hex_color.lstrip('#')
    rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    darkened = tuple(max(int(c * (1 - factor)), min_dark) for c in rgb)
    return '#' + ''.join(f'{c:02x}' for c in darkened)


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile', username=user.username)
    else:
        form = UserCreationForm()
    return render(request, 'Accounts/register.html', {'form': form})

@login_required
def profile(request, username):
    user = get_object_or_404(User, username=username)
    is_following = False
    profile = user.profile

    if request.method == 'POST' and request.user == user:
        profile.color_accent = request.POST.get('color_accent', profile.color_accent)
        profile.color_accent_light = request.POST.get('color_accent_light', profile.color_accent_light)
        profile.color_accent_dark = request.POST.get('color_accent_dark', profile.color_accent_dark)
        profile.color_contrast_color = request.POST.get('color_contrast_color', profile.color_contrast_color)
        profile.save()
        return redirect('profile', username=username)

    if request.user.is_authenticated:
        is_following = Follower.objects.filter(follower=request.user, following=user).exists()
        following_users = Follower.objects.filter(follower=request.user).values_list('following', flat=True)

    posts_query = Post.objects.filter(author=user)

    if user.profile.is_banned:
        posts = posts_query.filter(visibility='PUBLIC')
    elif request.user.is_authenticated and request.user == user:
        posts = posts_query
    elif request.user.is_authenticated and is_following:
        posts = posts_query.filter(Q(visibility='PUBLIC') | Q(visibility='FOLLOWERS'))
    else:
        posts = posts_query.filter(visibility='PUBLIC')

    posts = posts.order_by('-created_at').prefetch_related('react_set')

    for post in posts:
        reaction_counts = post.react_set.values('type').annotate(count=Count('type'))
        post.reaction_counts = {item['type']: item['count'] for item in reaction_counts}

        post.user_reacted_type = None
        if request.user.is_authenticated:
            user_reaction = post.react_set.filter(user=request.user).first()
            if user_reaction:
                post.user_reacted_type = user_reaction.type

    followers_count = Follower.objects.filter(following=user).count()
    following_count = Follower.objects.filter(follower=user).count()

    context = {
        'user': user,
        'profile': profile,
        'posts': posts,
        'is_following': is_following,
        'followers_count': followers_count,
        'following_count': following_count,
    }

    return render(request, 'Accounts/profile.html', context)

@login_required
def profile_update(request):
    if request.user.profile.is_banned:
        return render(request, 'Accounts/banned.html')

    profile = request.user.profile

    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            accent = profile.color_accent
            profile.color_accent_light = lighten_color(accent, 0.4)
            profile.color_accent_dark = darken_color(accent, 0.3)
            profile.save()

            return redirect('profile', username=request.user.username)

    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render(request, 'Accounts/profile_update.html', context)

@login_required
def follow_user(request, username):
    user_to_follow = get_object_or_404(User, username=username)
    Follower.objects.get_or_create(follower=request.user, following=user_to_follow)
    return redirect('profile', username=username)

@login_required
def unfollow_user(request, username):
    user_to_unfollow = get_object_or_404(User, username=username)
    Follower.objects.filter(follower=request.user, following=user_to_unfollow).delete()
    return redirect('profile', username=username)

def custom_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.profile.is_banned:
                    return render(request, 'Accounts/login.html',
                                  {'form': form, 'error_message': 'Your account has been suspended.'})

                login(request, user)
                return redirect('profile', username=user.username)
    else:
        form = AuthenticationForm()
    return render(request, 'Accounts/login.html', {'form': form})



def profile_view(request, username):
    user = get_object_or_404(User, username=username)
    profile = user.profile
    posts = Post.objects.filter(author=user).order_by('-created_at')

    context = {
        'user': user,
        'profile': profile,
        'posts': posts,
    }
    return render(request, 'profile.html', context)