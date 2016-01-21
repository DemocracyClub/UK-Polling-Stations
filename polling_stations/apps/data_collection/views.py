from django.views.generic import ListView

from .models import DataQuality


class LeagueTable(ListView):
    model = DataQuality
    queryset = DataQuality.objects.all().select_related('council')\
        .defer('council__area', 'council__location')
