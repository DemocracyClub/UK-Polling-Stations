from django.views.generic import ListView

from .models import DataQuality


class LeagueTable(ListView):
    model = DataQuality
    queryset = DataQuality.objects.order_by('-rating')
