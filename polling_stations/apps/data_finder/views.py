import re
import requests

from operator import itemgetter

from django.contrib.gis.geos import Point
from django.core.urlresolvers import reverse
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.views.generic import FormView, DetailView, TemplateView
from django.utils.translation import ugettext as _

from councils.models import Council
from data_finder.models import LoggedPostcode
from pollingstations.models import (
    PollingStation,
    ResidentialAddress
)
from whitelabel.views import WhiteLabelTemplateOverrideMixin
from .forms import PostcodeLookupForm, AddressSelectForm
from .helpers import (
    geocode,
    PostcodeError,
    DirectionsHelper
)

# sort a list of tuples by key in natural/human order
def natural_sort(l, key):
    convert = lambda text: int(text) if text.isdigit() else text
    alphanum_key = lambda item: [ convert(c) for c in re.split('([0-9]+)', key(item)) ]
    return sorted(l, key = alphanum_key)


class LogLookUpMixin(object):
    def log_postcode(self, postcode, context):
        kwargs = {
            'postcode': postcode,
            'had_data': bool(context['we_know_where_you_should_vote']),
            'location': context['location'],
            'council': context['council'],
            'brand': self.request.brand,
        }
        kwargs.update(self.request.session['utm_data'])
        LoggedPostcode.objects.create(**kwargs)


class HomeView(WhiteLabelTemplateOverrideMixin, FormView):
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


class BasePollingStationView(TemplateView, LogLookUpMixin):
    template_name = "postcode_view.html"


class PostcodeView(BasePollingStationView):

    def get_context_data(self, **context):
        try:
            l = geocode(self.kwargs['postcode'])
        except PostcodeError as e:
            context['error'] = e
            return context

        context['location'] = Point(l['wgs84_lon'], l['wgs84_lat'])

        context['council'] = Council.objects.get(
            area__covers=context['location'])

        context['station'] = PollingStation.objects.get_polling_station(
            context['location'],
            context['council'].council_id
        )

        if context['station'] and context['station'].location:
            dh = DirectionsHelper()
            context['directions'] = dh.get_directions(
                start_postcode=self.kwargs['postcode'],
                start_location=context['location'],
                end_location=context['station'].location,
            )

        context['we_know_where_you_should_vote'] = context.get('station')

        self.log_postcode(self.kwargs['postcode'], context)

        return context


class AddressView(BasePollingStationView):

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
        station = None
        if stations:
            station = stations[0]

        # council
        council = Council.objects.get(
            pk=address.council_id
        )

        # Geocode residential address grid ref
        # AddressView is a bit different to PostcodeView here
        # Failure to look up postcode in mapit is not fatal
        try:
            location = geocode(address.postcode)
            context['location'] = Point(location['wgs84_lon'], location['wgs84_lat'])
        except PostcodeError:
            context['location'] = None

        # assemble directions url
        if context and station.location and address.postcode:
            dh = DirectionsHelper()
            context['directions'] = dh.get_directions(
                start_postcode=address.postcode,
                start_location=context['location'],
                end_location=station.location,
            )

        # assemble context variables
        context['postcode'] = address.postcode
        context['station'] = station
        context['we_know_where_you_should_vote'] = station
        context['council'] = council
        self.log_postcode(address.postcode, context)
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
