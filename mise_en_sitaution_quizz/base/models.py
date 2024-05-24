from django.db import models
from django.contrib.auth.models import User


class Group(models.Model):
    name = models.CharField(max_length=100)
    members = models.ManyToManyField(User, related_name='custom_groups')

    def __str__(self):
        return self.name


class Quiz(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_quizzes')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class GroupQuizAttempt(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='quiz_attempts')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='group_attempts')
    started_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.group.name} - {self.quiz.title}'


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    text = models.CharField(max_length=500)

    def __str__(self):
        return self.text

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text

class QuizAttempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quiz_attempts')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='attempts')
    score = models.IntegerField()
    completed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.quiz.title}'

class UserAnswer(models.Model):
    attempt = models.ForeignKey(QuizAttempt, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.attempt.user.username} - {self.question.text} - {self.choice.text}'

    class Meta:
        unique_together = ('attempt', 'question')  # Ensure only one answer per question per attempt


class UserQuizAttempt(models.Model):
    group_attempt = models.ForeignKey(GroupQuizAttempt, on_delete=models.CASCADE, related_name='user_attempts')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='group_user_attempts')
    score = models.IntegerField()
    completed_at = models.DateTimeField(auto_now_add=True)
    duration = models.DurationField(null=True, blank=True)  # To track time taken to complete the quiz

    def __str__(self):
        return f'{self.user.username} - {self.group_attempt.quiz.title}'


class GroupUserAnswer(models.Model):
    user_attempt = models.ForeignKey(UserQuizAttempt, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user_attempt.user.username} - {self.question.text} - {self.choice.text}'

    class Meta:
        unique_together = ('user_attempt', 'question')  # Ensure only one answer per question per user attempt
#Player class
class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='player')
    pseudo = models.CharField(max_length=100)
    score = models.IntegerField(default=0)

    def __str__(self):
        return self.pseudo
def create_player_for_new_user(sender, instance, created, **kwargs):
    if created:
        Player.objects.create(user=instance, pseudo=instance.username)