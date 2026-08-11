from django.contrib import admin
from .models import Complaint


@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'user',
        'category',
        'location',
        'priority',
        'status',
        'assigned_staff',
        'created_at',
    )

    list_filter = (
        'category',
        'priority',
        'status',
    )

    search_fields = (
        'description',
        'location',
        'user__username',
    )