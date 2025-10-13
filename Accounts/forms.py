from django import forms
from django.contrib.auth.models import User
from .models import Profile


class ProfileThemeForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['color_accent', 'color_accent_light', 'color_accent_dark', 'bg_main', 'bg_sidebar']
        widgets = {
            'color_accent': forms.TextInput(attrs={'type': 'color'}),
            'color_accent_light': forms.TextInput(attrs={'type': 'color'}),
            'color_accent_dark': forms.TextInput(attrs={'type': 'color'}),
            'bg_main': forms.TextInput(attrs={'type': 'color'}),
            'bg_sidebar': forms.TextInput(attrs={'type': 'color'}),
        }
class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_picture', 'bio' , 'profile_banner' , 'color_accent']