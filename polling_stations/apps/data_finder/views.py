import abc
import json
import re
import requests

from operator import itemgetter

from django.conf import settings
from django.contrib.gis.geos import Point
from django.core.urlresolvers import reverse
from django.core.validators import validate_email
from django.forms import ValidationError
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404
from django.views.generic import FormView, DetailView, TemplateView
from django.utils import translation
from django.utils.translation import ugettext as _

from councils.models import Council
from data_finder.models import LoggedPostcode, CampaignSignup
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
    AddressSorter,
    PostcodeError,
    RateLimitError,
    RoutingHelper
)


class LogLookUpMixin(object):
    def log_postcode(self, postcode, context, view_used):

        if 'language' in context:
            language = context['language']
        else:
            language = self.get_language()

        if 'brand' in context:
            brand = context['brand']
        else:
            brand = self.request.brand

        kwargs = {
            'postcode': postcode,
            'had_data': bool(context['we_know_where_you_should_vote']),
            'location': context['location'],
            'council': context['council'],
            'brand': brand,
            'language': language,
            'view_used': view_used,
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

    def form_invalid(self, form):
        context = self.get_context_data(form=form)
        context['postcode'] = form.data['postcode']
        return self.render_to_response(context)


class PrivacyView(WhiteLabelTemplateOverrideMixin, TemplateView):
    template_name = "privacy.html"


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

    def get_language(self):
        if self.request.session and\
            translation.LANGUAGE_SESSION_KEY in self.request.session and\
            self.request.session[translation.LANGUAGE_SESSION_KEY]:
            return self.request.session[translation.LANGUAGE_SESSION_KEY]
        else:
            return ''

    def get_context_data_northern_ireland(self, **context):
        # special case for Northern Ireland
        context['postcode'] = self.postcode
        context['location'] = self.location
        context['council'] = None
        context['station'] = None
        context['directions'] = None
        context['we_know_where_you_should_vote'] = False
        context['noindex'] = True
        self.log_postcode(self.postcode, context, type(self).__name__)
        return context

    def get_context_data(self, **context):
        context['tile_layer'] = settings.TILE_LAYER
        context['mq_key'] = settings.MQ_KEY

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
            self.gss_codes = l['gss_codes']
            self.council_gss = l['council_gss']

        if self.postcode[:2] == 'BT' or 'N07000001' in self.gss_codes:
            # this postcode is in Northern Ireland
            context['custom'] = CustomFinder.objects.get_custom_finder(
                l['gss_codes'], self.postcode)
            if context['custom'] is None:
                raise Http404
            return self.get_context_data_northern_ireland(**context)

        self.council = self.get_council()
        self.station = self.get_station()
        self.directions = self.get_directions()

        context['postcode'] = self.postcode
        context['location'] = self.location
        context['council'] = self.council
        context['station'] = self.station
        context['directions'] = self.directions
        context['we_know_where_you_should_vote'] = self.station
        context['noindex'] = True

        if not context['we_know_where_you_should_vote']:
            if l is None:
                context['custom'] = None
            else:
                context['custom'] = CustomFinder.objects.get_custom_finder(
                    l['gss_codes'], self.postcode)

        self.log_postcode(self.postcode, context, type(self).__name__)

        return context


class PostcodeView(BasePollingStationView):

    def get(self, request, *args, **kwargs):

        if 'postcode' in request.GET:
            self.kwargs['postcode'] = kwargs['postcode'] = request.GET['postcode']
        if 'postcode' not in kwargs:
            return HttpResponseRedirect(reverse('home'))

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
        if getattr(self, 'council_gss'):
            try:
                return Council.objects.defer("area", "location").get(
                    council_id=self.council_gss)
            except Council.DoesNotExist:
                pass

        if getattr(self, 'gss_codes'):
            try:
                return Council.objects.defer("area", "location").get(
                    council_id__in=self.gss_codes)
            except Council.DoesNotExist:
                pass

        return Council.objects.get(
            area__covers=self.location)

    def get_station(self):
        return PollingStation.objects.get_polling_station(
            self.council.council_id, location=self.location)


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
        return Council.objects.defer("area", "location").get(
            pk=self.address.council_id)

    def get_station(self):
        if not self.address.polling_station_id:
            return None
        return PollingStation.objects.get_polling_station_by_id(
            self.address.polling_station_id,
            self.address.council_id)


class WeDontKnowView(PostcodeView):

    def get(self, request, *args, **kwargs):
        self.postcode = kwargs['postcode']
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def get_station(self):
        return None


def campaign_signup(request, postcode):
    if request.POST.get('join', 'false') == 'true':
        join_list = True
    else:
        join_list = False
    name = request.POST.get('name', '')
    email = request.POST.get('email', '')

    errors = { 'errors': { 'name': 0, 'email': 0 } }
    if not name or len(name) > 100:
        errors['errors']['name'] = 1
    if not email or len(email) > 100:
        errors['errors']['email'] = 1
    try:
        validate_email(email)
    except ValidationError:
        errors['errors']['email'] = 1

    if errors['errors']['name'] == 1 or errors['errors']['email'] == 1:
        return HttpResponse(json.dumps(errors),
            status=400, content_type='application/json')

    kwargs = {
        'postcode': postcode,
        'name': name,
        'email': email,
        'join_list': join_list
    }
    CampaignSignup.objects.create(**kwargs)

    return HttpResponse(json.dumps(errors),
        status=200, content_type='application/json')


class AddressFormView(FormView):
    form_class = AddressSelectForm
    template_name = "address_select.html"

    def get_context_data(self, **kwargs):
        context = super(AddressFormView, self).get_context_data(**kwargs)
        context['noindex'] = True
        return context

    def get_form(self, form_class):
        addresses = ResidentialAddress.objects.filter(
            postcode=self.kwargs['postcode']
        )

        select_addresses = [(element.slug, element.address) for element in addresses]
        sorter = AddressSorter()
        select_addresses = sorter.natural_sort(select_addresses, itemgetter(1))

        if not addresses:
            raise Http404
        else:
            return form_class(select_addresses, self.kwargs['postcode'], **self.get_form_kwargs())

    def form_valid(self, form):
        self.success_url = reverse(
            'address_view',
            kwargs={'address_slug': form.cleaned_data['address']}
        )
        return super(AddressFormView, self).form_valid(form)


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
