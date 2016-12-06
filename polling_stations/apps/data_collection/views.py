import requests
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
        .defer('council__area', 'council__location')\
        .annotate(has_report=Case(
                When(Q(report=''), then=Value(0)),
                When(~Q(report=''), then=Value(1)),
                output_field=IntegerField()
            )
        )\
        .order_by('-has_report', 'council__name')


class MorphReport(TemplateView):
    template_name = 'data_collection/morph_report.html'

    def get_timestamp_message(self, message, timestamp):
        """
        Used for printing a messages like
        'bla bla bla [date] (N days ago)'
        """
        date_formatted = datetime.strftime(timestamp, '%Y-%m-%d')
        date_human = TimeHelper.days_ago(timestamp)
        return message % (date_formatted, date_human)

    def query(self):
        url = "https://api.morph.io/wdiv-scrapers/dc-meta-scraper/data.json"
        url += "?key=%s&query=select%%20*%%20from%%20%%27report%%27%%3B"
        url = url % (settings.MORPH_API_KEY)

        res = requests.get(url)
        if res.status_code != 200:
            res.raise_for_status()
        return res.json()

    def get_context_data(self, **context):
        data = self.query()
        context = { 'data': [] }
        for council in data:
            started_polling = TimeHelper.parse_timestamp(council['started_polling'])
            council['started_polling'] = self.get_timestamp_message(
                '%s<br />(%s days ago)', started_polling)

            last_changed = TimeHelper.parse_timestamp(council['last_changed'])
            council['last_changed'] = self.get_timestamp_message(
                '%s<br />(%s days ago)', last_changed)

            context['data'].append(council)

        return context


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
