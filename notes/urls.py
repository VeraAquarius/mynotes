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

]