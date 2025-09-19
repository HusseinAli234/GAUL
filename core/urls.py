# core/urls.py (обновленный)
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('words/', views.words_list, name='words_list'),
    path('forum/', views.forum, name='forum'),
    path('forum/topic/<int:topic_id>/', views.forum_topic, name='forum_topic'),
    path('forum/create/', views.create_topic, name='create_topic'),
    path('forum/topic/<int:topic_id>/reply/', views.add_message, name='add_message'),
    path('profile/', views.profile, name='profile'),
    path('register/', views.register, name='register'),
    path('buy/<int:word_id>/', views.buy_word, name='buy_word'),
    path('rename/<int:word_id>/', views.rename_word, name='rename_word'),
]