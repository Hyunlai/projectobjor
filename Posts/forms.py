from django import forms
from .models import Post, Comment

class PostForm(forms.ModelForm):
    clear_image = forms.BooleanField(required=False, label="Remove current image")

    class Meta:
        model = Post
        fields = ['caption', 'image', 'video', 'visibility']

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields['image'].required = False
        self.fields['video'].required = False

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']