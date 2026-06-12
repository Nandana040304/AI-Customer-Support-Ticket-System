from django.contrib import admin
from .models import Ticket


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'user',
        'title',
        'category',
        'status',
        'created_at'
    )

    list_filter = (
        'status',
        'category'
    )

    search_fields = (
        'title',
        'description',
        'user__username'
    )

    ordering = (
        '-created_at',
    )