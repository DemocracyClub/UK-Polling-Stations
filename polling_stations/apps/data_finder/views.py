import re
import requests

from operator import itemgetter

from django.contrib.gis.geos import Point
from django.core.urlresolvers import reverse
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.views.generic import FormView, DetailView, TemplateView

from councils.models import Council
from pollingstations.models import (
    PollingDistrict,
    PollingStation,
    ResidentialAddress
)
from .forms import PostcodeLookupForm, AddressSelectForm
from .helpers import geocode


base_google_url = "https://maps.googleapis.com/maps/api/directions/json?mode=walking&units=imperial&origin="

def build_directions_url(postcode, y, x):
    url = "{base_url}{postcode}&destination={destination}".format(
            base_url=base_google_url,
            postcode=postcode,
            destination="{0},{1}".format(y, x),
        )
    return url

# sort a list of tuples by key in natural/human order
def natural_sort(l, key):
    convert = lambda text: int(text) if text.isdigit() else text
    alphanum_key = lambda item: [ convert(c) for c in re.split('([0-9]+)', key(item)) ]
    return sorted(l, key = alphanum_key)


class HomeView(FormView):
    form_class = PostcodeLookupForm
    template_name = "home.html"

    def form_valid(self, form):

        postcode = form.cleaned_data['postcode'].replace(' ', '')

        addresses = ResidentialAddress.objects.filter(
            postcode=postcode
        )

        if addresses:
            distinct_stations = ResidentialAddress\
                .objects\
                .filter(postcode=postcode)\
                .values('polling_station_id')\
                .distinct()

            if len(distinct_stations) == 1:
                # all the addresses in this postcode
                # map to one polling station
                self.success_url = reverse(
                    'address_view',
                    kwargs={'address_id': addresses[0].id}
                )
            elif len(distinct_stations) > 1:
                # addresses in this postcode map to
                # multiple polling stations
                self.success_url = reverse(
                    'address_select_view',
                    kwargs={'postcode': postcode}
                )
            else:
                return super(HomeView, self).form_valid(form)

        else:
            # postcode is not in ResidentialAddress table
            self.success_url = reverse(
                'postcode_view',
                kwargs={'postcode': postcode}
            )
        return super(HomeView, self).form_valid(form)


class PostcodeView(TemplateView):
    template_name = "postcode_view.html"


    def get_points(self, areas):
        if areas['polling_district'].polling_station_id:
            stations = PollingStation.objects.filter(internal_council_id=
                    areas['polling_district'].polling_station_id)
            if stations:
                return stations

        stations = PollingStation.objects.filter(
            location__within=areas['polling_district'].area)
        if stations:
            return stations

        return PollingStation.objects.filter(
            location__within=areas['council'].area)



    def get_context_data(self, **context):
        l = geocode(self.kwargs['postcode'])
        context['location'] = Point(l['wgs84_lon'], l['wgs84_lat'])
        context['points'] = []

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
            context['points'] = self.get_points(areas)

        if context and context['points']:
            url = build_directions_url(
                context['postcode'],
                context['points'][0].location.y,
                context['points'][0].location.x
            )
            context['directions'] = requests.get(url).json()

        context['we_know_where_you_should_vote'] = context['points'] and context['has_polling_district']
        context['only_polling_stations'] = context['points'] and (not context['has_polling_district'])
        context['only_polling_districts'] = (not context['points']) and context['has_polling_district']
        context['no_data'] = (not context['points']) and (not context['has_polling_district'])
        context['areas'] = areas
        context['council'] = areas['council']
        return context


class AddressView(TemplateView):
    template_name = "postcode_view.html"

    def get_context_data(self, **context):

        # address
        address = get_object_or_404(
            ResidentialAddress,
            pk=self.kwargs['address_id']
        )

        # polling station
        stations = PollingStation.objects.filter(
            internal_council_id=address.polling_station_id
        )

        # council
        areas = {}
        areas['council'] = Council.objects.get(
            pk=address.council_id
        )

        # assemble directions url
        if context and stations[0].location:
            url = build_directions_url(
                address.postcode,
                stations[0].location.y,
                stations[0].location.x
            )
            context['directions'] = requests.get(url).json()

        # geocode residential address grid ref
        location = geocode(address.postcode)

        # assemble context variables
        context['location'] = Point(location['wgs84_lon'], location['wgs84_lat'])
        context['has_polling_district'] = False
        context['postcode'] = address.postcode
        context['points'] = stations
        context['we_know_where_you_should_vote'] = context['points']
        context['no_data'] = (not context['points']) and (not context['has_polling_district'])
        #context['areas'] = areas
        context['council'] = areas['council']
        return context


class AddressFormView(FormView):
    form_class = AddressSelectForm
    template_name = "address_select.html"

    def get_form(self, form_class):
        addresses = ResidentialAddress.objects.filter(
            postcode=self.kwargs['postcode']
        )

        select_addresses = [(element.id, element.address) for element in addresses]
        select_addresses = natural_sort(select_addresses, itemgetter(1))

        if not addresses:
            raise Http404
        else:
            return form_class(select_addresses, **self.get_form_kwargs())

    def form_valid(self, form):
        self.success_url = reverse(
            'address_view',
            kwargs={'address_id': form.cleaned_data['address']}
        )
        return super(AddressFormView, self).form_valid(form)


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
