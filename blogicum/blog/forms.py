from django import forms
from .models import Post, Comments
from datetime import datetime as dt


DATE_FORMAT = '{:%Y-%m-%d %H:%M}'


class PostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['pub_date'].initial = DATE_FORMAT.format(dt.now())

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
