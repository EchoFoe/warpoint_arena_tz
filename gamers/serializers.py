from rest_framework import serializers
from django.urls import reverse
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import permissions
from .models import Team, Player, Fraction


class PlayersSerializer(serializers.ModelSerializer):

    teams_name = serializers.SerializerMethodField()
    relative_url = serializers.SerializerMethodField()
    url = serializers.HyperlinkedIdentityField(view_name='gamers:player-detail')
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    class Meta:
        model = Player
        fields = ('relative_url', 'url', 'pk', 'last_name', 'first_name', 'middle_name', 'photo', 'player_role',
                  'progress_points', 'teams_name', 'team')

    def get_teams_name(self, obj):
        return '%s (id=%s)' % (obj.team.name, obj.team.pk)

    def get_relative_url(self, obj):
        return reverse('gamers:player-detail', args=[obj.id])


class FractionsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Fraction
        fields = ('pk', 'name', 'players_list', 'created')


class TeamsSerializer(serializers.ModelSerializer):

    players_count = serializers.SerializerMethodField()
    total_points = serializers.SerializerMethodField()
    url = serializers.HyperlinkedIdentityField(view_name='gamers:team-detail')

    class Meta:
        model = Team
        fields = ('pk', 'url', 'name', 'players_count', 'total_points')

    def get_players_count(self, obj):
        return obj.players.count()

    def get_total_points(self, obj):
        total_points = sum(item.progress_points for item in obj.players.filter(is_active=True))
        return total_points


class TeamDetailSerializer(serializers.ModelSerializer):
    fractions = FractionsSerializer(many=True)

    class Meta:
        model = Team
        fields = ('pk', 'name', 'fractions')
