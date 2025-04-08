# notes/forms.py
from django import forms
from .models import Note,Tag, Comment,Category,Reminder,Collaborator
from django.contrib.auth.forms import UserCreationForm,PasswordChangeForm
from django.contrib.auth.models import User
from django.utils import timezone


class CollaboratorForm(forms.Form):
    email = forms.EmailField(label='协作用户邮箱')

    def __init__(self, *args, **kwargs):
        self.note = kwargs.pop('note', None)
        super().__init__(*args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise forms.ValidationError("用户不存在")
        if Collaborator.objects.filter(note=self.note, user=user).exists():
            raise forms.ValidationError("用户已经是协作用户")
        return email


class ReminderForm(forms.ModelForm):
    class Meta:
        model = Reminder
        widgets = {
            'reminder_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
        fields = ['reminder_time']

    def clean_reminder_time(self):
        reminder_time = self.cleaned_data['reminder_time']
        if reminder_time < timezone.now():
            raise forms.ValidationError("提醒时间不能早于当前时间")
        return reminder_time


class NoteForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    class Meta:
        model = Note
        fields = ['title', 'content', 'category','tags']


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']


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


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class EmailUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email']

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exclude(id=self.instance.id).exists():
            raise forms.ValidationError('此邮箱已被使用')
        return email


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

class CustomPasswordChangeForm(PasswordChangeForm):
    pass




