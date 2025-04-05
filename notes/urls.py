# notes/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('welcome/', views.welcome, name='welcome'),
    # path('create/', views.create_note, name='create'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('create/', views.create_note, name='create_note'),  # 新增URL
    path('delete/<int:note_id>/', views.delete_note, name='delete_note'),
    path('search/', views.search_notes, name='search_notes'),
    path('advanced_search/', views.advanced_search, name='advanced_search'),
    path('create_tag/', views.create_tag, name='create_tag'),
    path('edit/<int:note_id>/', views.edit_note, name='edit_note'),
    path('tags/', views.tag_list, name='tag_list'),
    path('tags/create/', views.create_tag, name='create_tag'),
    path('export/', views.export_notes, name='export_notes'),
    path('export/pdf/', views.export_to_pdf, name='export_to_pdf'),
    path('<int:note_id>/', views.note_detail, name='note_detail'),
    path('delete_comment/<int:comment_id>/', views.delete_comment, name='delete_comment'),
    path('edit_comment/<int:comment_id>/', views.edit_comment, name='edit_comment'),
    path('comment_history/<int:comment_id>/', views.comment_history, name='comment_history'),
    path('comment_detail/<int:comment_id>/', views.comment_detail, name='comment_detail'),
    path('trash/', views.trash, name='trash'),
    path('recover/<int:note_id>/', views.recover_note, name='recover_note'),
    path('permanent_delete/<int:note_id>/', views.permanent_delete_note, name='permanent_delete_note'),
    path('empty_trash/', views.empty_trash, name='empty_trash'),
    path('empty_trash/success/', views.empty_trash_success, name='empty_trash_success'),
    path('share/<int:note_id>/', views.share_note, name='share_note'),
    path('shared/<int:note_id>/', views.shared_note, name='shared_note'),
    path('sharable_notes/', views.view_sharable_notes, name='view_sharable_notes'),
    path('email_test/', views.send_email_test, name='email_test'),
    path('update_email/', views.update_email, name='update_email'),
    path('profile/', views.profile, name='profile'),
    path('update_profile/', views.update_profile, name='update_profile'),
    path('change_password/', views.change_password, name='change_password'),
    path('backup/', views.backup_notes, name='backup_notes'),
    path('restore/', views.restore_notes, name='restore_notes'),

]