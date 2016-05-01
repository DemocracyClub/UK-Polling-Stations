import abc
import re
import requests

from operator import itemgetter

from django.contrib.gis.geos import Point
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404
from django.views.generic import FormView, DetailView, TemplateView
from django.utils.translation import ugettext as _

from councils.models import Council
from data_finder.models import LoggedPostcode
from pollingstations.models import (
    PollingStation,
    ResidentialAddress,
    CustomFinder
)
from whitelabel.views import WhiteLabelTemplateOverrideMixin
from .forms import PostcodeLookupForm, AddressSelectForm
from .helpers import (
    geocode,
    DirectionsHelper,
    natural_sort,
    PostcodeError,
    RateLimitError,
    RoutingHelper
)


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

        rh = RoutingHelper(postcode)
        endpoint = rh.get_endpoint()
        self.success_url = reverse(
            endpoint.view,
            kwargs=endpoint.kwargs
        )

        return super(HomeView, self).form_valid(form)


class BasePollingStationView(
    TemplateView, LogLookUpMixin, metaclass=abc.ABCMeta):

    template_name = "postcode_view.html"

    @abc.abstractmethod
    def get_location(self):
        pass

    @abc.abstractmethod
    def get_council(self):
        pass

    @abc.abstractmethod
    def get_station(self):
        pass

    def get_directions(self):
        if self.postcode and self.station and self.station.location:
            dh = DirectionsHelper()
            return dh.get_directions(
                start_postcode=self.postcode,
                start_location=self.location,
                end_location=self.station.location,
            )
        else:
            return None

    def get_context_data(self, **context):
        try:
            l = self.get_location()
        except (PostcodeError, RateLimitError) as e:
            context['error'] = str(e)
            return context

        if l is None:
            # AddressView.get_location() may legitimately return None
            self.location = None
        else:
            self.location = Point(l['wgs84_lon'], l['wgs84_lat'])

        self.council = self.get_council()
        self.station = self.get_station()
        self.directions = self.get_directions()

        context['postcode'] = self.postcode
        context['location'] = self.location
        context['council'] = self.council
        context['station'] = self.station
        context['directions'] = self.directions
        context['we_know_where_you_should_vote'] = self.station

        if not context['we_know_where_you_should_vote']:
            if l is None:
                context['custom'] = None
            else:
                context['custom'] = CustomFinder.objects.get_custom_finder(l['gss_codes'], self.postcode)

        self.log_postcode(self.postcode, context)
        return context


class PostcodeView(BasePollingStationView):

    def get(self, request, *args, **kwargs):
        rh = RoutingHelper(self.kwargs['postcode'])
        endpoint = rh.get_endpoint()
        if endpoint.view != 'postcode_view':
            return HttpResponseRedirect(
                reverse(endpoint.view, kwargs=endpoint.kwargs)
            )
        else:
            # we are already in postcode_view
            self.postcode = kwargs['postcode']
            context = self.get_context_data(**kwargs)
            return self.render_to_response(context)

    def get_location(self):
        return geocode(self.postcode)

    def get_council(self):
        return Council.objects.get(
            area__covers=self.location)

    def get_station(self):
        return PollingStation.objects.get_polling_station(
            self.location, self.council.council_id)


class AddressView(BasePollingStationView):

    def get(self, request, *args, **kwargs):
        self.address = get_object_or_404(
            ResidentialAddress,
            slug=self.kwargs['address_slug']
        )
        self.postcode = self.address.postcode
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def get_location(self):
        try:
            location = geocode(self.postcode)
            return location
        except PostcodeError:
            return None

    def get_council(self):
        return Council.objects.get(
            pk=self.address.council_id)

    def get_station(self):
        return PollingStation.objects.get_polling_station_by_id(
            self.address.polling_station_id,
            self.address.council_id)


class AddressFormView(FormView):
    form_class = AddressSelectForm
    template_name = "address_select.html"

    def get_form(self, form_class):
        addresses = ResidentialAddress.objects.filter(
            postcode=self.kwargs['postcode']
        )

        select_addresses = [(element.slug, element.address) for element in addresses]
        select_addresses = natural_sort(select_addresses, itemgetter(1))

        if not addresses:
            raise Http404
        else:
            return form_class(select_addresses, **self.get_form_kwargs())

    def form_valid(self, form):
        self.success_url = reverse(
            'address_view',
            kwargs={'address_slug': form.cleaned_data['address']}
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
