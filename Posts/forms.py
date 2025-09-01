from django import forms
from .models import Post, Comment

class PostForm(forms.ModelForm):
    # Allows the user to clear the existing image uploaded
    clear_image = forms.BooleanField(required=False, label="Remove current image")

    class Meta:
        model = Post
        fields = ['caption', 'image']

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        # Make the 'image' field optional
        self.fields['image'].required = False

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']