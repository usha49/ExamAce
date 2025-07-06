from django.contrib import admin

# Register your models here.
from .models import MCQ, TestResult

@admin.register(MCQ)
class MCQAdmin(admin.ModelAdmin):
    list_display = ('question', 'topic', 'difficulty', 'chapter')
    list_filter = ('chapter','difficulty')

@admin.register(TestResult)
class TestResultAdmin(admin.ModelAdmin):
    list_display = ('user','score','date_taken')
    list_filter = ('user','date_taken')
    ordering = ('date_taken',)  