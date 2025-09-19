# core/admin.py
from django.contrib import admin
from .models import UserProfile, Word, WordHistory, ForumTopic, ForumMessage

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'first_name', 'last_name', 'balance']

@admin.register(Word)
class WordAdmin(admin.ModelAdmin):
    list_display = ['name', 'current_name', 'price', 'owner', 'change_count']

@admin.register(WordHistory)
class WordHistoryAdmin(admin.ModelAdmin):
    list_display = ['word', 'old_name', 'new_name', 'changed_by', 'changed_at']

@admin.register(ForumTopic)
class ForumTopicAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_by', 'created_at']

@admin.register(ForumMessage)
class ForumMessageAdmin(admin.ModelAdmin):
    list_display = ['topic', 'author', 'created_at']