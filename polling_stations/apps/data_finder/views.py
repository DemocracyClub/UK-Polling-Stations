import requests

from django.contrib.gis.geos import Point
from django.core.urlresolvers import reverse
from django.views.generic import FormView, DetailView, TemplateView

from councils.models import Council
from pollingstations.models import PollingDistrict, PollingStation
from .forms import PostcodeLookupForm
from .helpers import geocode

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
            areas['neighbours'] = PollingDistrict.objects.filter(area__touches=areas['polling_district'].area)
            context['has_polling_district'] = True
        except PollingDistrict.DoesNotExist:
            context['has_polling_district'] = False

        if context['has_polling_district']:
            context['points'] = PollingStation.objects.filter(location__within=areas['polling_district'].area)
        else:
            context['points'] = PollingStation.objects.filter(location__within=areas['council'].area)

        if context['points']:
            base_url = "https://maps.googleapis.com/maps/api/directions/json?mode=walking&units=imperial&origin="
            context['directions'] = requests.get(
                "{base_url}{postcode}&destination={destination}".format(
                    base_url=base_url,
                    postcode=context['postcode'],
                    destination=context['points'][0].postcode,
                )).json()


        context['areas'] = areas
        return context


class CouncilView(DetailView):
    model = Council