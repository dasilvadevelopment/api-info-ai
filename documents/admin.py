from django.contrib import admin

from .models import Document


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'title', 'department', 'uploaded_by',
        'is_active', 'replaces', 'uploaded_at',
    ]
    list_filter = ['is_active', 'department', 'uploaded_at']
    search_fields = ['title', 'checksum']
    date_hierarchy = 'uploaded_at'
    readonly_fields = ['checksum', 'uploaded_at']

