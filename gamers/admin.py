from django.contrib import admin
from .models import Team, Player, Fraction


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    save_as = True
    fields = ['name', 'is_active', 'created']
    list_display = ['name', 'is_active', 'created']
    search_fields = ['name', 'players__last_name']
    list_editable = ['is_active']
    date_hierarchy = 'created'
    list_filter = ['players__player_role', 'is_active', 'created']
    readonly_fields = ['created']


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    save_as = True
    fields = [('last_name', 'first_name', 'middle_name'), 'player_role', 'photo', 'progress_points', 'team',
              'is_active', 'created']
    list_display = ['photo_img', 'full_name', 'player_role', 'progress_points', 'team', 'is_active', 'created']
    list_display_links = ['full_name']
    search_fields = ['last_name']
    list_editable = ['progress_points', 'team', 'is_active']
    date_hierarchy = 'created'
    list_filter = ['team', 'is_active', 'created']
    readonly_fields = ['created']


@admin.register(Fraction)
class FractionAdmin(admin.ModelAdmin):
    save_as = True
    filter_horizontal = ['players_list']
    fields = ['name', 'team', 'leader', 'players_list', 'is_active', 'created']
    list_display = ['name', 'team', 'is_active']
    list_display_links = ['name']
    readonly_fields = ['created']
