from django.shortcuts import render, redirect, get_object_or_404
from Posts.models import Post
from django.contrib.auth.models import User
from .models import Admin
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth.decorators import user_passes_test

@user_passes_test(lambda u: u.is_staff)
def redirect_admin_root(request):
    return redirect('/admin/dashboard/')

def admin_dashboard(request):
    try:
        if request.user.is_authenticated and Admin.objects.get(user=request.user).is_admin:
            posts = Post.objects.all().order_by('-created_at')
            return render(request, 'Admin/admin_dashboard.html', {'posts': posts})
    except Admin.DoesNotExist:
        return redirect('home')

@login_required
def ban_user(request, username):
    try:
        if request.user.is_authenticated and Admin.objects.get(user=request.user).is_admin:
            user_to_ban = get_object_or_404(User, username=username)
            user_to_ban.profile.is_banned = True
            user_to_ban.profile.save()
            return redirect('admin_dashboard')
    except Admin.DoesNotExist:
        return redirect('home')

@login_required
def unban_user(request, username):
    try:
        if request.user.is_authenticated and Admin.objects.get(user=request.user).is_admin:
            user_to_unban = get_object_or_404(User, username=username)
            user_to_unban.profile.is_banned = False
            user_to_unban.profile.save()
            return redirect('admin_dashboard')
    except Admin.DoesNotExist:
        return redirect('home')

@login_required
def delete_post(request, post_id):
    try:
        if request.user.is_authenticated and Admin.objects.get(user=request.user).is_admin:
            post = get_object_or_404(Post, pk=post_id)
            post.delete()
            return redirect('admin_dashboard')
    except Admin.DoesNotExist:
        return redirect('home')