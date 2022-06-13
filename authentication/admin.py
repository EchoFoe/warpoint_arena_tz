from django.contrib import admin
from .models import User


@admin.register(User)
class TariffAdmin(admin.ModelAdmin):
    save_as = True
    fields = [('username', 'email'), 'is_active', 'is_staff', 'is_superuser', ('created_at', 'updated_at')]
    list_display = ['username', 'email', 'is_active', 'is_staff', 'is_superuser', 'created_at']
    list_display_links = ['username']
    search_fields = ['username', 'email']
    list_editable = ['is_active']
    list_filter = ['is_active', 'created_at', 'updated_at']
    date_hierarchy = 'created_at'
    readonly_fields = ['is_staff', 'is_superuser', 'created_at', 'updated_at']
