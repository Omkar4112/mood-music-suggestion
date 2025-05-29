from django.db import models
from django.contrib.auth.models import AbstractUser

# Custom user model extending AbstractUser
class User(AbstractUser):
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username

class Mood(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Song(models.Model):
    title = models.CharField(max_length=200)
    artist = models.CharField(max_length=100)
    genre = models.CharField(max_length=100)
    url = models.URLField()
    duration = models.CharField(max_length=10)  # e.g., "3:45"
    image = models.URLField(blank=True, null=True)  # Optional song image URL

    moods = models.ManyToManyField(Mood, through='MoodSongMap', related_name='songs')

    def __str__(self):
        return f"{self.title} - {self.artist}"

class MoodSongMap(models.Model):
    # changed related_name to avoid clash
    mood = models.ForeignKey(Mood, on_delete=models.CASCADE, related_name="mood_song_maps")
    song = models.ForeignKey(Song, on_delete=models.CASCADE, related_name="mood_song_maps")

    def __str__(self):
        return f"{self.mood.name} - {self.song.title}"

class UserMoodHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="mood_history")
    mood = models.ForeignKey(Mood, on_delete=models.CASCADE, related_name="user_histories")
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.mood.name} at {self.timestamp}"
