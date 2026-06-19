from django.contrib import admin
from .models import Rating

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ['id', 'job', 'customer', 'rider', 'score', 'created_at']
    list_filter  = ['score']