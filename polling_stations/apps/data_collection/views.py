from datetime import datetime
from django.conf import settings
from django.db.models import Case, IntegerField, Q, Value, When
from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView, TemplateView
from .models import DataQuality


class LeagueTable(ListView):
    model = DataQuality
    queryset = DataQuality.objects\
        .all()\
        .select_related('council')\
        .defer('council__area')\
        .annotate(has_report=Case(
                When(Q(report=''), then=Value(0)),
                When(~Q(report=''), then=Value(1)),
                output_field=IntegerField()
            )
        )\
        .order_by('-has_report', 'council__name')


def data_quality(request, council_id):
    data = get_object_or_404(DataQuality.objects.select_related('council'),
        pk=council_id)
    context = {
        'summary': data
    }
    return render(request, 'data_collection/dataquality_detail.html', context)


class TimeHelper:

    @staticmethod
    def parse_timestamp(timestamp, tz=True):
        if tz:
            return datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S.%f+00:00')
        else:
            return datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S.%f')

    @staticmethod
    def days_ago(timestamp):
        return abs(datetime.utcnow() - timestamp).days
