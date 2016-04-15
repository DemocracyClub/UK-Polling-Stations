from django.db.models import Case, IntegerField, Q, Value, When
from django.views.generic import ListView
from .models import DataQuality


class LeagueTable(ListView):
    model = DataQuality
    queryset = DataQuality.objects\
        .all()\
        .select_related('council')\
        .defer('council__area', 'council__location')\
        .annotate(has_report=Case(
                When(Q(report=''), then=Value(1)),
                When(~Q(report=''), then=Value(0)),
                output_field=IntegerField()
            )
        )\
        .order_by('has_report', 'council__name')
