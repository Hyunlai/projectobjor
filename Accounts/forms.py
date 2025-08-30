from django import forms
from django.contrib.auth.models import User
from .models import Profile

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):
    # Add a caption field for the new post
    caption = forms.CharField(max_length=255, required=False, help_text="Add a caption for your new profile picture post.")

    class Meta:
        model = Profile
        fields = ['bio', 'profile_picture']