from django import forms
from .models import Post, Comments


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = '__all__'
        exclude = ('author',)
        widgets = {
            'pub_date': forms.DateTimeInput(attrs={'type': 'datetime-local'},),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ('text',)
