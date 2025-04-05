from django.contrib.auth.models import User
from django.shortcuts import render
from django.template.loader import render_to_string

# Create your views here.
# notes/views.py
from .models import Note,Tag,Comment, CommentHistory, SharedNote
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .forms import (NoteForm,TagForm,CommentForm,ShareNoteForm,CustomUserCreationForm,
                    EmailUpdateForm, CustomPasswordChangeForm,ProfileForm)
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator
from reportlab.pdfgen import canvas
from io import BytesIO
import markdown
from xhtml2pdf import pisa
from io import BytesIO
from .utils import font_patch  # 导入字体设置函数
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages


def welcome(request):
    return HttpResponse("欢迎来到我的笔记应用！")

# def index(request):
#     notes = Note.objects.all()
#     return render(request, 'notes/index.html', {'notes': notes})

def create_note(request):
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = NoteForm()
    return render(request, 'notes/create_note.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            # user = form.save()
            form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'notes/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('index')
    else:
        form = AuthenticationForm()
    return render(request, 'notes/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('login')

# @login_required
# def index(request):
#     notes = Note.objects.filter(user=request.user)
#     return render(request, 'notes/index.html', {'notes': notes})

@login_required
def index(request):
    notes = Note.objects.filter(user=request.user,is_deleted=False).order_by('-created_at')
    paginator = Paginator(notes, 5)  # 每页显示5条笔记
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'notes/index.html', {'page_obj': page_obj})

@login_required
def create_note(request):
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user  # 将当前用户关联到笔记
            note.save()
            form.save_m2m()  # 保存多对多关系
            return redirect('index')
    else:
        form = NoteForm()
    return render(request, 'notes/create_note.html', {'form': form})

@login_required
def delete_note(request, note_id):
    note = get_object_or_404(Note, id=note_id)
    if note.user != request.user:
        return redirect('index')  # 非创建者重定向
    if request.method == 'POST':
        note.is_deleted = True
        note.save()
        return redirect('index')
    return render(request, 'notes/delete_note.html', {'note': note})

@login_required
def edit_note(request, note_id):
    note = get_object_or_404(Note, id=note_id)
    if note.user != request.user:
        return redirect('index')  # 非创建者重定向
    if request.method == 'POST':
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = NoteForm(instance=note)
    return render(request, 'notes/edit_note.html', {'form': form})

def search_notes(request):
    query = request.GET.get('q', '')
    notes = Note.objects.filter(
        Q(title__icontains=query) | Q(content__icontains=query)
    )
    return render(request, 'notes/search_results.html', {'notes': notes, 'query': query})


def advanced_search(request):
    query = request.GET.get('q', '')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    tags = request.GET.get('tags')

    notes = Note.objects.all()

    if query:
        notes = notes.filter(Q(title__icontains=query) | Q(content__icontains=query))
    if start_date:
        notes = notes.filter(created_at__gte=start_date)
    if end_date:
        notes = notes.filter(created_at__lte=end_date)
    if tags:
        notes = notes.filter(tags__name__in=tags).distinct()

    all_tags = Tag.objects.all()

    return render(request, 'notes/advanced_search.html', {
        'notes': notes,
        'query': query,
        'start_date': start_date,
        'end_date': end_date,
        'selected_tags': tags,
        'all_tags': all_tags
    })


@login_required
def create_tag(request):
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = TagForm()
    return render(request, 'notes/create_tag.html', {'form': form})


@login_required
def create_tag(request):
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tag_list')
    else:
        form = TagForm()
    return render(request, 'notes/create_tag.html', {'form': form})

@login_required
def tag_list(request):
    tags = Tag.objects.all()
    return render(request, 'notes/tag_list.html', {'tags': tags})


@login_required
def export_notes(request):
    if request.method == 'POST':
        format = request.POST.get('format')
        notes = Note.objects.filter(user=request.user)
        if format == 'pdf':
            return export_to_pdf(notes)
        elif format == 'markdown':
            return export_to_markdown(notes)
    return render(request, 'notes/export.html')

# def export_to_pdf(notes):
#     buffer = BytesIO()
#     c = canvas.Canvas(buffer)
#     c.setFont("Helvetica", 12)
#     y = 750  # Starting position for text
#     for note in notes:
#         c.drawString(50, y, f"标题: {note.title}")
#         c.drawString(50, y - 15, f"内容: {note.content}")
#         c.drawString(50, y - 30, f"创建时间: {note.created_at}")
#         y -= 50  # Move down for the next note
#         if y < 50:  # New page if there's no more space
#             c.showPage()
#             y = 750
#     c.save()
#     buffer.seek(0)
#     response = HttpResponse(buffer, content_type='application/pdf')
#     response['Content-Disposition'] = 'attachment; filename="notes.pdf"'
#     return response

@login_required
def export_to_pdf(request):
    notes = Note.objects.filter(user=request.user)
    font_patch()  # 调用字体设置函数

    buffer = BytesIO()
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="notes.pdf"'

    html = render_to_string('notes/pdf_template.html', {'notes': notes})
    pisa_status = pisa.CreatePDF(html, dest=response, encoding='utf-8')

    if pisa_status.err:
        return HttpResponse('PDF生成失败')
    return response


def export_to_markdown(notes):
    markdown_text = "# 我的笔记\n\n"
    for note in notes:
        markdown_text += f"## {note.title}\n\n{note.content}\n\n创建时间: {note.created_at}\n\n---\n\n"
    response = HttpResponse(markdown_text, content_type='text/markdown')
    response['Content-Disposition'] = 'attachment; filename="notes.md"'
    return response



@login_required
def note_detail(request, note_id):
    note = get_object_or_404(Note, id=note_id)
    comments = Comment.objects.filter(note=note).order_by('-created_at')
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.note = note
            comment.user = request.user
            comment.save()
            return redirect('note_detail', note_id=note_id)
    else:
        form = CommentForm()
    return render(request, 'notes/note_detail.html', {'note': note, 'comments': comments, 'form': form})

@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if comment.user != request.user:
        return redirect('note_detail', note_id=comment.note.id)
    if request.method == 'POST':
        comment.delete()
        return redirect('note_detail', note_id=comment.note.id)
    return render(request, 'notes/delete_comment.html', {'comment': comment})

@login_required
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if comment.user != request.user:
        return redirect('note_detail', note_id=comment.note.id)
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            # 记录历史
            CommentHistory.objects.create(comment=comment, content=comment.content)
            form.save()
            return redirect('note_detail', note_id=comment.note.id)
    else:
        form = CommentForm(instance=comment)
    return render(request, 'notes/edit_comment.html', {'form': form, 'comment': comment})


@login_required
def comment_history(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    histories = CommentHistory.objects.filter(comment=comment).order_by('-changed_at')
    return render(request, 'notes/comment_history.html', {'histories': histories, 'comment': comment})


@login_required
def comment_detail(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    return render(request, 'notes/comment_detail.html', {'comment': comment})



@login_required
def recover_note(request, note_id):
    note = get_object_or_404(Note, id=note_id)
    if note.user != request.user:
        return redirect('trash')
    if request.method == 'POST':
        note.is_deleted = False
        note.save()
        return redirect('index')
    return render(request, 'notes/recover_note.html', {'note': note})

@login_required
def trash(request):
    notes = Note.objects.filter(user=request.user, is_deleted=True)
    return render(request, 'notes/trash.html', {'notes': notes})

@login_required
def permanent_delete_note(request, note_id):
    note = get_object_or_404(Note, id=note_id)
    if note.user != request.user:
        return redirect('trash')
    if request.method == 'POST':
        note.delete()
        return redirect('trash')
    return render(request, 'notes/permanent_delete_note.html', {'note': note})


@login_required
def empty_trash(request):
    if request.method == 'POST':
        notes = Note.objects.filter(user=request.user, is_deleted=True)
        notes.delete()
        return redirect('empty_trash_success')
    return render(request, 'notes/empty_trash.html')

@login_required
def empty_trash_success(request):
    return render(request, 'notes/empty_trash_success.html')


@login_required
def share_note(request, note_id):
    note = get_object_or_404(Note, id=note_id)
    if note.user != request.user:
        return redirect('index')
    if request.method == 'POST':
        form = ShareNoteForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                recipient = User.objects.get(email=email)
                SharedNote.objects.create(note=note, shared_with=recipient, shared_by=request.user)
                # 发送邮件通知
                send_mail(
                    '笔记分享',
                    f'用户{request.user.username}分享了一篇笔记给您: http://127.0.0.1:8000/notes/shared/{note.id}/',
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                    fail_silently=False,
                )
                return render(request, 'notes/share_success.html', {'note': note})
            except User.DoesNotExist:
                return render(request, 'notes/share_note.html', {'form': form, 'note': note, 'error': '用户不存在'})
    else:
        form = ShareNoteForm()
    return render(request, 'notes/share_note.html', {'form': form, 'note': note})


@login_required
def shared_note(request, note_id):
    note = get_object_or_404(Note, id=note_id)
    shared_notes = SharedNote.objects.filter(note=note, shared_with=request.user)
    if not shared_notes.exists() and note.user != request.user:
        return redirect('index')
    return render(request, 'notes/shared_note.html', {'note': note})


@login_required
def view_sharable_notes(request):
    notes = Note.objects.filter(user=request.user, is_deleted=False)
    return render(request, 'notes/sharable_notes.html', {'notes': notes})


def send_email_test(request):
    send_mail(
        '测试邮件',
        '这是一封测试邮件。',
        settings.DEFAULT_FROM_EMAIL,
        ['15821886267@163.com'],
        fail_silently=False,
    )
    return render(request, 'notes/email_test.html')


@login_required
def update_email(request):
    if request.method == 'POST':
        form = EmailUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, '邮箱已更新')
            return redirect('profile')
    else:
        form = EmailUpdateForm(instance=request.user)
    return render(request, 'notes/update_email.html', {'form': form})



@login_required
def profile(request):
    shared_notes = SharedNote.objects.filter(shared_by=request.user)
    return render(request, 'notes/profile.html', {'shared_notes': shared_notes})

@login_required
def update_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, '个人资料已更新')
            return redirect('profile')
    else:
        form = ProfileForm(instance=request.user)
    return render(request, 'notes/update_profile.html', {'form': form})


@login_required
def change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '密码已更新')
            return redirect('profile')
    else:
        form = CustomPasswordChangeForm(user=request.user)
    return render(request, 'notes/change_password.html', {'form': form})


