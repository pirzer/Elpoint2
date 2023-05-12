from .models import Post, Comment, Tag 
from django import forms


class PostForm(forms.ModelForm):
    """
    Form model that allows authenticated users to
    add and save posts
    """
    class Meta:
        model = Post
        fields = ('title', 'tag', 'content',)

        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Enter a title'}),
            'tag': forms.Select(),
            'content': forms.Textarea(
                attrs={'placeholder': 'Write Post here'})
        }

class CommentForm(forms.ModelForm):
    """
    Form model that allows authenticated users to
    submit comments on posts
    """
    class Meta:
        model = Comment
        fields = ('body',)