import abc
import json
import requests

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
from data_finder.models import (
    LoggedPostcode,
    CampaignSignup,
    ElectionNotificationSignup
)
from pollingstations.models import (
    PollingStation,
    ResidentialAddress,
    CustomFinder
)
from pollingstations.helpers import format_postcode_no_space
from whitelabel.views import WhiteLabelTemplateOverrideMixin
from .forms import PostcodeLookupForm, AddressSelectForm
from .helpers import (
    AddressSorter,
    DirectionsHelper,
    get_council,
    get_territory,
    geocode,
    EveryElectionWrapper,
    MultipleCouncilsException,
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
        if 'api_user' in context:
            kwargs['api_user'] = context['api_user']
        kwargs.update(self.request.session['utm_data'])
        LoggedPostcode.objects.create(**kwargs)


class LanguageMixin(object):

    def get_language(self):
        if self.request.session and\
            translation.LANGUAGE_SESSION_KEY in self.request.session and\
            self.request.session[translation.LANGUAGE_SESSION_KEY]:
            return self.request.session[translation.LANGUAGE_SESSION_KEY]
        else:
            return ''


class HomeView(WhiteLabelTemplateOverrideMixin, FormView):
    form_class = PostcodeLookupForm
    template_name = "home.html"

    def form_valid(self, form):

        postcode = format_postcode_no_space(form.cleaned_data['postcode'])

        rh = RoutingHelper(postcode)
        endpoint = rh.get_endpoint()
        self.success_url = reverse(
            endpoint.view,
            kwargs=endpoint.kwargs
        )

        return super(HomeView, self).form_valid(form)

    def form_invalid(self, form):
        context = self.get_context_data(form=form)
        context['postcode'] = form.data.get('postcode', '')
        return self.render_to_response(context)


class PrivacyView(WhiteLabelTemplateOverrideMixin, TemplateView):
    template_name = "privacy.html"


class BasePollingStationView(
    TemplateView, LogLookUpMixin, LanguageMixin, metaclass=abc.ABCMeta):

    template_name = "postcode_view.html"

    @abc.abstractmethod
    def get_location(self):
        pass

    @abc.abstractmethod
    def get_council(self, geocode_result):
        pass

    @abc.abstractmethod
    def get_station(self):
        pass

    def get_directions(self):
        if self.location and self.station and self.station.location:
            dh = DirectionsHelper()
            return dh.get_directions(
                start_location=self.location,
                end_location=self.station.location,
            )
        else:
            return None

    def get_context_data(self, **context):
        context['tile_layer'] = settings.TILE_LAYER
        context['mq_key'] = settings.MQ_KEY

        try:
            loc = self.get_location()
        except (PostcodeError, RateLimitError) as e:
            context['error'] = str(e)
            return context

        if loc is None:
            # AddressView.get_location() may legitimately return None
            self.location = None
        else:
            self.location = Point(loc['wgs84_lon'], loc['wgs84_lat'])

        self.council = self.get_council(loc)
        self.station = self.get_station()
        self.directions = self.get_directions()

        ee = EveryElectionWrapper(self.postcode)
        if settings.EVERY_ELECTION['CHECK']:
            context['has_election'] = ee.has_election()
        else:
            context['has_election'] = settings.EVERY_ELECTION['HAS_ELECTION']

        if not context['has_election']:
            context['error'] = 'There are no upcoming elections in your area'
        context['election_explainers'] = ee.get_explanations()

        context['postcode'] = self.postcode
        context['location'] = self.location
        context['council'] = self.council
        context['station'] = self.station
        context['directions'] = self.directions
        context['we_know_where_you_should_vote'] = self.station
        context['noindex'] = True
        context['territory'] = get_territory(self.postcode)
        if not context['we_know_where_you_should_vote']:
            if loc is None:
                context['custom'] = None
            else:
                context['custom'] = CustomFinder.objects.get_custom_finder(
                    loc['gss_codes'], self.postcode)

        self.log_postcode(self.postcode, context, type(self).__name__)

        return context


class PostcodeView(BasePollingStationView):

    def get(self, request, *args, **kwargs):

        if 'postcode' in request.GET:
            self.kwargs['postcode'] = kwargs['postcode'] = request.GET['postcode']
        if 'postcode' not in kwargs or kwargs['postcode'] == '':
            return HttpResponseRedirect(reverse('home'))
        self.kwargs['postcode'] = kwargs['postcode'] = format_postcode_no_space(kwargs['postcode'])

        rh = RoutingHelper(self.kwargs['postcode'])
        endpoint = rh.get_endpoint()
        if endpoint.view != 'postcode_view':
            return HttpResponseRedirect(
                reverse(endpoint.view, kwargs=endpoint.kwargs)
            )
        else:
            # we are already in postcode_view
            self.postcode = kwargs['postcode']

            try:
                context = self.get_context_data(**kwargs)
            except MultipleCouncilsException:
                return HttpResponseRedirect(
                    reverse('multiple_councils_view',
                    kwargs={'postcode': self.postcode})
                )

            return self.render_to_response(context)

    def get_location(self):
        return geocode(self.postcode)

    def get_council(self, geocode_result):
        return get_council(geocode_result)

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

        try:
            context = self.get_context_data(**kwargs)
        except MultipleCouncilsException:
            return HttpResponseRedirect(
                reverse('multiple_councils_view',
                kwargs={'postcode': self.postcode})
            )

        return self.render_to_response(context)

    def get_location(self):
        try:
            location = geocode(self.postcode)
            return location
        except PostcodeError:
            return None

    def get_council(self, geocode_result):
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


class MultipleCouncilsView(TemplateView, LogLookUpMixin, LanguageMixin):
    # because sometimes "we don't know" just isn't uncertain enough
    template_name = "multiple_councils.html"

    def get(self, request, *args, **kwargs):
        rh = RoutingHelper(self.kwargs['postcode'])
        endpoint = rh.get_endpoint()
        if endpoint.view != 'multiple_councils_view':
            return HttpResponseRedirect(
                reverse(endpoint.view, kwargs=endpoint.kwargs)
            )

        self.council_ids = rh.councils
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def get_context_data(self, **context):
        context['councils'] = []
        for council_id in self.council_ids:
            context['councils'].append(Council.objects.get(pk=council_id))

        context['territory'] = get_territory(self.kwargs['postcode'])

        log_data = {
            'we_know_where_you_should_vote': False,
            'location': None,
            'council': None,
        }
        self.log_postcode(self.kwargs['postcode'], log_data, type(self).__name__)

        return context


def signup(request, postcode, model, fields):
    if request.POST.get('join', 'false') == 'true':
        join_list = True
    else:
        join_list = False
    name = request.POST.get('name', '')
    email = request.POST.get('email', '')

    errors = { 'errors': { 'name': 0, 'email': 0 } }

    if 'name' in fields:
        if not name or len(name) > 100:
            errors['errors']['name'] = 1

    if 'email' in fields:
        if not email or len(email) > 100:
            errors['errors']['email'] = 1
        try:
            validate_email(email)
        except ValidationError:
            errors['errors']['email'] = 1

    if (errors['errors']['name'] == 1 and 'name' in fields) or\
        (errors['errors']['email'] == 1 and 'email' in fields):
        return HttpResponse(json.dumps(errors),
            status=400, content_type='application/json')

    kwargs = { 'postcode': postcode, 'join_list': join_list }
    if 'name' in fields:
        kwargs['name'] = name
    if 'email' in fields:
        kwargs['email'] = email

    model.objects.create(**kwargs)

    return HttpResponse(json.dumps(errors),
        status=200, content_type='application/json')


def election_notification_signup(request, postcode):
    return signup(request, postcode, ElectionNotificationSignup, ['email'])


def campaign_signup(request, postcode):
    return signup(request, postcode, CampaignSignup, ['name', 'email'])


class AddressFormView(FormView):
    form_class = AddressSelectForm
    template_name = "address_select.html"
    NOTINLIST = '519RA5LCGuHHXQvBUVgOXiCcqWy7SZG1inRDKcx1'

    def get_context_data(self, **kwargs):
        context = super(AddressFormView, self).get_context_data(**kwargs)
        context['noindex'] = True
        return context

    def get_form(self, form_class):
        addresses = ResidentialAddress.objects.filter(
            postcode=self.kwargs['postcode']
        )

        if not addresses:
            raise Http404

        sorter = AddressSorter(addresses)
        addresses = sorter.natural_sort()
        select_addresses = [(element.slug, element.address) for element in addresses]
        select_addresses.append((self.NOTINLIST, 'My address is not in the list'))
        return form_class(select_addresses, self.kwargs['postcode'], **self.get_form_kwargs())

    def form_valid(self, form):
        slug = form.cleaned_data['address']
        if slug == self.NOTINLIST:
            self.success_url = reverse(
                'we_dont_know',
                kwargs={'postcode': self.kwargs['postcode']}
            )
        else:
            self.success_url = reverse(
                'address_view',
                kwargs={'address_slug': slug}
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
