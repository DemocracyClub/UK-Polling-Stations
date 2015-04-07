import requests

from django.contrib.gis.geos import Point
from django.core.urlresolvers import reverse
from django.views.generic import FormView, DetailView, TemplateView

from councils.models import Council
from pollingstations.models import PollingDistrict, PollingStation
from .forms import PostcodeLookupForm
from .helpers import geocode

base_google_url = "https://maps.googleapis.com/maps/api/directions/json?mode=walking&units=imperial&origin="

class HomeView(FormView):
    form_class = PostcodeLookupForm
    template_name = "home.html"

    def form_valid(self, form):
        postcode = form.cleaned_data['postcode'].replace(' ', '')
        self.success_url = reverse(
            'postcode_view', kwargs={'postcode': postcode})
        return super(HomeView, self).form_valid(form)

class PostcodeView(TemplateView):
    template_name = "postcode_view.html"

    def get_context_data(self, **context):
        l = geocode(self.kwargs['postcode'])
        context['location'] = Point(l['wgs84_lon'], l['wgs84_lat'])

        areas = {}
        areas['council'] = Council.objects.get(
            area__covers=context['location'])

        try:
            areas['polling_district'] = PollingDistrict.objects.get(
                area__covers=context['location'])
            areas['neighbours'] = PollingDistrict.objects.filter(
                area__touches=areas['polling_district'].area)
            context['has_polling_district'] = True
        except PollingDistrict.DoesNotExist:
            context['has_polling_district'] = False

        if context['has_polling_district']:
            context['points'] = PollingStation.objects.filter(
                location__within=areas['polling_district'].area)
        else:
            context['points'] = PollingStation.objects.filter(
                location__within=areas['council'].area)

        if context['points']:
            context['directions'] = requests.get(
                "{base_url}{postcode}&destination={destination}".format(
                    base_url=base_google_url,
                    postcode=context['postcode'],
                    destination=context['points'][0].postcode,
                )).json()

        context['we_know_where_you_should_vote'] = context['points'] and context['has_polling_district']
        context['only_polling_stations'] = context['points'] and (not context['has_polling_district'])
        context['only_polling_districts'] = (not context['points']) and context['has_polling_district']
        context['no_data'] = (not context['points']) and (not context['has_polling_district'])
        context['areas'] = areas
        context['council'] = areas['council']
        return context


class CouncilView(DetailView):
    model = Council

class CoverageView(TemplateView):
    template_name = 'coverage.html'

    def get_context_data(self, *a, **k):
        context = super(CoverageView, self).get_context_data(*a, **k)
        num_councils  = Council.objects.count()
        districts, stations = 0, 0
        covered = []
        for council in Council.objects.all():
            if council.pollingstation_set.count() > 1:
                stations += 1
                covered.append(council)
            if council.pollingdistrict_set.count() > 1:
                districts += 1

        context['num_councils']          = num_councils
        context['num_district_councils'] = districts
        context['perc_districts']        = "%d%%" % (float(districts) / num_councils * 100)
        context['num_station_councils']  = stations
        context['perc_stations']         = "%d%%" % (float(stations) / num_councils * 100)
        context['covered']               = covered
        return context
