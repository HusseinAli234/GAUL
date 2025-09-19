# core/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import UserProfile, Word, WordHistory, ForumTopic, ForumMessage
from django.utils import timezone
from django.core.paginator import Paginator

def index(request):
    words = Word.objects.all()[:3]
    return render(request, 'core/index.html', {'words': words})

def words_list(request):
    words = Word.objects.all()
    paginator = Paginator(words, 6)  # по 6 слов на страницу

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "core/words.html", {
        "words": page_obj,
        "page_obj": page_obj,
    })

def forum(request):
    topics = ForumTopic.objects.all()
    return render(request, 'core/forum.html', {'topics': topics})

def forum_topic(request, topic_id):
    topic = get_object_or_404(ForumTopic, id=topic_id)
    messages = ForumMessage.objects.filter(topic=topic)
    return render(request, 'core/forum_topic.html', {'topic': topic, 'messages': messages})

@login_required
def profile(request):
    user_profile = UserProfile.objects.get(user=request.user)
    owned_words = Word.objects.filter(owner=user_profile)
    return render(request, 'core/profile.html', {
        'profile': user_profile,
        'owned_words': owned_words
    })

# core/views.py (обновленная функция register)
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        phone_number = request.POST.get('phone_number', '')
        telegram_username = request.POST.get('telegram_username', '')
        
        user = User.objects.create_user(username=username, password=password, email=email)
        user_profile = UserProfile.objects.get(user=user)
        user_profile.first_name = first_name
        user_profile.last_name = last_name
        user_profile.phone_number = phone_number
        user_profile.telegram_username = telegram_username
        user_profile.save()
        
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('index')
    
    return render(request, 'core/register.html')

@login_required
def buy_word(request, word_id):
    word = get_object_or_404(Word, id=word_id)
    user_profile = UserProfile.objects.get(user=request.user)
    
    if user_profile.balance >= word.price:
        user_profile.balance -= word.price
        user_profile.save()
        
        # Transfer ownership
        if word.owner:
            previous_owner = word.owner
            previous_owner.balance += word.price
            previous_owner.save()
        
        word.owner = user_profile
        word.save()
    
    return redirect('words_list')

@login_required
def rename_word(request, word_id):
    if request.method == 'POST':
        word = get_object_or_404(Word, id=word_id)
        user_profile = UserProfile.objects.get(user=request.user)
        
        if word.owner == user_profile:
            new_name = request.POST['new_name']
            
            # Save history
            WordHistory.objects.create(
                word=word,
                old_name=word.current_name,
                new_name=new_name,
                changed_by=user_profile
            )
            
            word.current_name = new_name
            word.change_count += 1
            word.save()
    
    return redirect('profile')

@login_required
def create_topic(request):
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        user_profile = UserProfile.objects.get(user=request.user)
        
        topic = ForumTopic.objects.create(
            title=title,
            created_by=user_profile
        )
        
        ForumMessage.objects.create(
            topic=topic,
            author=user_profile,
            content=content
        )
        
        return redirect('forum_topic', topic_id=topic.id)
    
    return render(request, 'core/create_topic.html')

@login_required
def add_message(request, topic_id):
    if request.method == 'POST':
        content = request.POST['content']
        user_profile = UserProfile.objects.get(user=request.user)
        topic = get_object_or_404(ForumTopic, id=topic_id)
        
        ForumMessage.objects.create(
            topic=topic,
            author=user_profile,
            content=content
        )
        
        return redirect('forum_topic', topic_id=topic_id)
    
    return redirect('forum_topic', topic_id=topic_id)