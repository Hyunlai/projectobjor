from django.shortcuts import render, redirect
from Posts.models import Post
from .models import Admin

# Create your views here.

def admin_dashboard(request):
    try:
        if request.user.is_authenticated and Admin.objects.get(user=request.user).is_admin:
            posts = Post.objects.all().order_by('-created_at')
            return render(request, 'admin/admin_dashboard.html', {'posts': posts})
    except Admin.DoesNotExist:
        return redirect('home')