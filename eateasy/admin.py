"""imports for admin page"""

from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Recipe, Comment, MealPlanItem


@admin.register(Recipe)
class RecipeAdmin(SummernoteModelAdmin):
    """Allows admin to manage recipes via the admin panel"""
    list_filter = ('status', 'created_on')
    list_display = ('title', 'slug', 'status', 'created_on')
    search_fields = ('title', 'description')
    summernote_fields = ('description', 'method')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Allows admin to manage comments on recipes via the admin panel"""
    list_display = ('name', 'body', 'recipe', 'created_on')
    list_filter = ('created_on',)
    search_fields = ('name', 'email', 'body')


@admin.register(MealPlanItem)
class MealplanAdmin(admin.ModelAdmin):
    """Allows admin to manage user meal plans via the admin panel"""
    list_display = ('user', 'recipe', 'day')
