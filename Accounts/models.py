from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(default='default/default.jpg', upload_to='profile_pics')
    profile_banner = models.ImageField(default='default/banner.jpg', upload_to='profile_banners')
    profile_song = models.FileField(upload_to='profile_song/', blank=True, null=True)
    bio = models.TextField(blank=True)
    is_banned = models.BooleanField(default=False)

    color_accent = models.CharField(max_length=7, default="#ff4da6")  # primary pink
    color_accent_light = models.CharField(max_length=7, default="#ffb3d9")  # lighter pink
    color_accent_dark = models.CharField(max_length=7, default="#ff80bf")  # dark pink
    bg_main = models.CharField(max_length=20, default="rgba(255,255,255,0.8)")  # main feed background
    bg_sidebar = models.CharField(max_length=20, default="rgba(255,179,217,0.6)")  # sidebars

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

class Follower(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'following')

    def __str__(self):
        return f"{self.follower.username} follows {self.following.username}"