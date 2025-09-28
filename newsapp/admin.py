from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Article

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ("english_title", "urdu_title", "section", "created_at")
    search_fields = ("english_title", "urdu_title", "section")
    list_filter = ("section", "created_at")
