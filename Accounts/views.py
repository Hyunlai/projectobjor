from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .forms import UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from Posts.models import Post, React
from django.db.models import Count
from .models import Profile, Follower
from django.db.models import Q
from Admin.models import Admin

# Create your views here.

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

def profile(request, username):
    user = get_object_or_404(User, username=username)
    is_following = False

    if request.user.is_authenticated:
        is_following = Follower.objects.filter(follower=request.user, following=user).exists()

    followers_count = Follower.objects.filter(following=user).count()
    following_count = Follower.objects.filter(follower=user).count()

    if user.profile.is_banned:
        posts = []
    else:
        posts = Post.objects.filter(author=user).order_by('-created_at')

    context = {
        'user': user,
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

    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile', username=request.user.username)
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

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