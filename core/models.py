# core/models.py
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=1000.00)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    telegram_username = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Word(models.Model):
    name = models.CharField(max_length=100, unique=True)
    current_name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=100.00)
    owner = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, blank=True)
    change_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.current_name

class WordHistory(models.Model):
    word = models.ForeignKey(Word, on_delete=models.CASCADE)
    old_name = models.CharField(max_length=100)
    new_name = models.CharField(max_length=100)
    changed_by = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True)
    changed_at = models.DateTimeField(auto_now_add=True)

class ForumTopic(models.Model):
    title = models.CharField(max_length=200)
    created_by = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class ForumMessage(models.Model):
    topic = models.ForeignKey(ForumTopic, on_delete=models.CASCADE)
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance, first_name="", last_name="")

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()