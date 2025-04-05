# notes/forms.py
from django import forms
from .models import Note,Tag, Comment

class NoteForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    class Meta:
        model = Note
        fields = ['title', 'content', 'tags']



class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['name']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']



class ShareNoteForm(forms.Form):
    email = forms.EmailField(label='分享给', required=True)

