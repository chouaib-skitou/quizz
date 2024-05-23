from django.contrib import admin
from .models import Player
from .models import Quiz, Question, Choice, QuizAttempt, UserAnswer
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('pseudo', 'user', 'score')

admin.site.register(Player,PlayerAdmin)
admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(QuizAttempt)
admin.site.register(UserAnswer)
