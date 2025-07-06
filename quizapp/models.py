from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class MCQ(models.Model):
    question = models.TextField()
    options = models.JSONField()  # Because the options are in a list like ['A', 'B', 'C', 'D']
    answer = models.CharField(max_length=255)
    explanation = models.TextField(blank=True, null=True)
    topic = models.CharField(max_length=255)
    difficulty = models.CharField(max_length=50)
    chapter = models.CharField(max_length=50)

    def __str__(self):
        return self.question[:50]  # Display first 50 characters in admin panel
    
class TestResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField()
    total = models.IntegerField()
    date_taken = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.score}/{self.total} on {self.date_taken}"
    