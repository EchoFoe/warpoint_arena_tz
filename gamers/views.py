from django.shortcuts import render
from rest_framework import filters, viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from .models import Team, Player, Fraction
from .serializers import PlayersSerializer, TeamsSerializer, FractionsSerializer, TeamDetailSerializer
from .throttles import CustomRateThrottle


def home(request):
    return render(request, 'home/home.html')


def players_list(request):
    players = Player.objects.filter(is_active=True)

    context = {
        'players': players,
    }

    return render(request, 'players/players_list.html', context)


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'


class PlayerList(viewsets.ModelViewSet):
    queryset = Player.objects.filter(is_active=True)
    # throttle_classes = [CustomRateThrottle]
    serializer_class = PlayersSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    filterset_fields = ['last_name', 'team_id']
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    search_fields = ['last_name', 'team__id']
    lookup_field = 'pk'


class TeamList(viewsets.ModelViewSet):
    queryset = Team.objects.filter(is_active=True)
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'list':
            return TeamsSerializer
        if self.action == 'retrieve':
            return TeamDetailSerializer
        return TeamsSerializer


class FractionList(viewsets.ModelViewSet):
    queryset = Fraction.objects.filter(is_active=True)
    serializer_class = FractionsSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'
