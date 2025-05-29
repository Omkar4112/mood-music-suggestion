from django.contrib import admin

from django.contrib import admin
from .models import Mood, Song, MoodSongMap, UserMoodHistory, User

admin.site.register(Mood)
admin.site.register(Song)
admin.site.register(MoodSongMap)
admin.site.register(UserMoodHistory)
admin.site.register(User)

