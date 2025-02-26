from django.contrib import admin

# Register your models here.
from .models import MCQ

@admin.register(MCQ)
class MCQAdmin(admin.ModelAdmin):
    list_display = ('question', 'topic', 'difficulty', 'chapter')