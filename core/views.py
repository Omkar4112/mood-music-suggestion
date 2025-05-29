from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from .models import Mood, Song, MoodSongMap, UserMoodHistory

User = get_user_model()

def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Uncomment below if you want to auto-login after signup:
            # login(request, user)
            return redirect('login')  # or redirect('home') if auto-logging in
        else:
            print("Signup errors:", form.errors)  # For debugging
    else:
        form = CustomUserCreationForm()
    return render(request, 'core/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'core/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def home(request):
    moods = Mood.objects.all()  # keep this as you said, no change
    songs = Song.objects.all()  # add all songs here
    return render(request, 'core/home.html', {'moods': moods, 'songs': songs})

@login_required
def profile(request):
    return render(request, 'core/profile.html')

@login_required
def mood_asking(request):
    moods = Mood.objects.all()
    return render(request, 'core/mood_asking.html', {'moods': moods})

@login_required
def suggest_songs(request):
    if request.method == 'POST':
        mood_id = request.POST.get('mood_id')
        mood = get_object_or_404(Mood, id=mood_id)
        UserMoodHistory.objects.create(user=request.user, mood=mood)
        songs = Song.objects.filter(mood_song_maps__mood=mood).distinct()
        return render(request, 'core/suggest.html', {'songs': songs, 'mood': mood})
    return redirect('mood_asking')
