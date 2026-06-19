from django.contrib import admin
from .models import Negotiation

@admin.register(Negotiation)
class NegotiationAdmin(admin.ModelAdmin):
    list_display = ['id', 'job', 'sender', 'receiver', 'amount', 'status', 'created_at']
    list_filter  = ['status']