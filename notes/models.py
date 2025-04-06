from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.

class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Note(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # 添加user字段
    tags = models.ManyToManyField(Tag, blank=True)  # 添加多对多关系
    is_deleted = models.BooleanField(default=False)  # 逻辑删除字段
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True) #分类字段
    word_count = models.IntegerField(default=0)  # 添加字数字段

    def __str__(self):
        return self.title

class Comment(models.Model):
    note = models.ForeignKey(Note, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.note.title}"

    @property
    def histories(self):
        return self.commenthistory_set.all().order_by('-changed_at')



class CommentHistory(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    content = models.TextField()
    changed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"History for comment {self.comment.id} at {self.changed_at}"

class SharedNote(models.Model):
    note = models.ForeignKey(Note, on_delete=models.CASCADE)
    shared_with = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shared_with')
    shared_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shared_by')
    shared_at = models.DateTimeField(auto_now_add=True)
    share_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    def __str__(self):
        return f"Shared {self.note.title} with {self.shared_with.username}"




