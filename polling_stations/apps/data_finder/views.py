import abc
from datetime import datetime
from typing import Optional

from addressbase.models import Address
from councils.models import Council
from django.conf import settings
from django.contrib.gis.geos import Point
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils import timezone, translation
from django.views.generic import FormView, TemplateView
from pollingstations.models import (
    AccessibilityInformation,
    CustomFinder,
    PollingStation,
)
from uk_geo_utils.geocoders import MultipleCodesException
from uk_geo_utils.helpers import AddressSorter, Postcode
from whitelabel.views import WhiteLabelTemplateOverrideMixin

from .forms import AddressSelectForm, PostcodeLookupForm
from .helpers import (
    DirectionsHelper,
    EveryElectionWrapper,
    PostcodeError,
    RoutingHelper,
    geocode,
    get_council,
)
from .helpers.every_election import (
    EmptyEveryElectionWrapper,
    StaticElectionsAPIElectionWrapper,
)


def polling_station_current(station):
    """
    Should pass in station object annotated with 'elections' - an array containing election dates.
    """
    if not station:
        return False
    if not getattr(station, "elections", None):
        return False
    try:
        latest_election_date = max(station.elections)
        if latest_election_date >= timezone.now().date():
            return True
    except TypeError:
        return False
    return False


class LogLookUpMixin(object):
    def log_postcode(self, postcode, context, view_used):
        if view_used != "api":
            # Log to firehose
            utm_data = {}

            if hasattr(self.request, "session"):
                utm_data = self.request.session.get("utm_data")

            entry = settings.POSTCODE_LOGGER.entry_class(
                postcode=postcode,
                dc_product=settings.POSTCODE_LOGGER.dc_product.wdiv,
                **utm_data,
            )

            settings.POSTCODE_LOGGER.log(entry)


class LanguageMixin(object):
    def get_language(self):
        if (
            self.request.session
            and translation in self.request.session
            and self.request.session[translation]
        ):
            return self.request.session[translation]
        return ""


def get_date_context(election_date: Optional[str]) -> dict:
    if election_date:
        election_date: datetime = timezone.make_aware(
            datetime.strptime(election_date, "%Y-%m-%d")
        )
        polls_close = election_date.replace(hour=22)
        now = timezone.now()
        return {
            "election_date": election_date,
            "election_date_is_today": election_date.date() == now.date(),
            "show_polls_open_card": now < polls_close,
        }

    return {"show_polls_open_card": False}


class HomeView(WhiteLabelTemplateOverrideMixin, FormView):
    form_class = PostcodeLookupForm
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["show_gb_id_messaging"] = getattr(
            settings, "SHOW_GB_ID_MESSAGING", False
        )

        charismatic_dates = getattr(settings, "NEXT_CHARISMATIC_ELECTION_DATES", [])
        try:
            election_date = charismatic_dates[0]
        except IndexError:
            election_date = None

        date_context = get_date_context(election_date)
        context.update(**date_context)

        return context

    def form_valid(self, form):
        postcode = Postcode(form.cleaned_data["postcode"])
        rh = RoutingHelper(postcode)
        # Don't preserve query, as the user has already been to an HTML page
        self.success_url = rh.get_canonical_url(self.request, preserve_query=False)

        return super(HomeView, self).form_valid(form)

    def form_invalid(self, form):
        context = self.get_context_data(form=form)
        context["postcode"] = form.data.get("postcode", "")
        return self.render_to_response(context)


class BasePollingStationView(
    TemplateView, LogLookUpMixin, LanguageMixin, metaclass=abc.ABCMeta
):
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

    def get_advance_voting_station(self):
        if not getattr(settings, "SHOW_ADVANCE_VOTING_STATIONS", False):
            return None
        if hasattr(self, "address"):
            return self.address.uprntocouncil.advance_voting_station
        return None

    def get_ee_wrapper(self, rh: RoutingHelper):
        if rh and rh.route_type == "multiple_addresses":
            return EmptyEveryElectionWrapper()
        if rh.elections_response:
            return StaticElectionsAPIElectionWrapper(rh.elections_response)
        if not self.location or self.location.tuple == (0.0, 0.0):
            return EveryElectionWrapper(postcode=self.postcode)
        return EveryElectionWrapper(point=self.location)

    def get_directions(self):
        if self.location and self.station and self.station.location:
            dh = DirectionsHelper()
            return dh.get_directions(
                start_location=self.location, end_location=self.station.location
            )
        return None

    def we_know_where_you_should_vote(self):
        return polling_station_current(self.get_station())

    def get_context_data(self, **context):
        context["tile_layer"] = settings.TILE_LAYER
        context["mq_key"] = settings.MQ_KEY

        try:
            loc = self.get_location()
        except PostcodeError as e:
            context["error"] = str(e)
            context["postcode_form"] = PostcodeLookupForm
            return context

        if loc is None:
            # AddressView.get_location() may legitimately return None
            self.location = None
        else:
            self.location = loc.centroid

        self.council = self.get_council(loc)
        self.station = self.get_station()
        context["has_at_station_info"] = False
        context["station_is_temporary"] = False
        if self.station:
            access_info: AccessibilityInformation = getattr(
                self.station, "accessibility_information", None
            )
            if access_info:
                context["has_at_station_info"] = access_info.has_at_station_info
                context["station_is_temporary"] = access_info.is_temporary

        self.directions = self.get_directions()

        ee = self.get_ee_wrapper(context.get("rh"))
        context["has_election"] = ee.has_election()
        context["multiple_elections"] = ee.multiple_elections
        context["election_explainers"] = ee.get_explanations()
        context["cancelled_election"] = ee.get_cancelled_election_info()
        context["advance_voting_station"] = self.get_advance_voting_station()
        context["requires_voter_id"] = ee.get_voter_id_status()

        context["postcode"] = self.postcode.with_space
        context["location"] = self.location
        context["council"] = self.council
        context["station"] = self.station
        context["directions"] = self.directions
        context["we_know_where_you_should_vote"] = self.we_know_where_you_should_vote()
        context["noindex"] = True
        context["territory"] = self.postcode.territory
        if not context["we_know_where_you_should_vote"]:
            if loc is None:
                context["custom"] = None
            else:
                try:
                    context["custom"] = CustomFinder.objects.get_custom_finder(
                        loc, self.postcode.without_space
                    )

                except MultipleCodesException:
                    context["custom"] = None

        self.log_postcode(self.postcode, context, type(self).__name__)

        return context


class PostcodeView(BasePollingStationView):
    def get(self, request, *args, **kwargs):
        if "postcode" in request.GET:
            self.kwargs["postcode"] = kwargs["postcode"] = request.GET["postcode"]
        if "postcode" not in kwargs or kwargs["postcode"] == "":
            return HttpResponseRedirect(reverse("home"))

        rh = RoutingHelper(self.kwargs["postcode"])
        kwargs["rh"] = rh

        if rh.view != "postcode_view":
            return HttpResponseRedirect(rh.get_canonical_url(request))

        # we are already in postcode_view
        self.postcode = Postcode(kwargs["postcode"])
        context = self.get_context_data(**kwargs)

        return self.render_to_response(context)

    def get_location(self):
        return geocode(self.postcode)

    def get_council(self, geocode_result):
        return get_council(geocode_result)

    def get_station(self):
        """
        We're in PostcodeView so either postcode isn't in addressbase,
        or if postcode is in addressbase we don't have station info for
        any of the uprns.
        Either way let's be explicit that station is None
        """
        return


class AddressView(BasePollingStationView):
    def get(self, request, *args, **kwargs):
        self.address = get_object_or_404(
            Address.objects.select_related("uprntocouncil"), uprn=self.kwargs["uprn"]
        )
        self.postcode = Postcode(self.address.postcode)
        context = self.get_context_data(**kwargs)

        return self.render_to_response(context)

    def get_location(self):
        return geocode(self.postcode)

    def get_council(self, geocode_result):
        return self.address.council

    def get_station(self):
        return self.address.polling_station_with_elections()

    def get_ee_wrapper(self, rh=None):
        return EveryElectionWrapper(point=self.address.location)


class ExamplePostcodeView(BasePollingStationView):

    """
    This class presents a hard-coded example of what our website does
    without having to worry about having any data imported
    or whether an election is actually happening or not
    """

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def get_location(self):
        return type(
            "Geocoder",
            (object,),
            {"centroid": Point(-2.54333651887832, 51.43921783606831, srid=4326)},
        )

    def get_council(self, geocode_result):
        return Council.objects.get(pk="BST")

    def get_station(self):
        ps = PollingStation(
            internal_council_id="BREF",
            postcode="BS4 4NZ",
            address="St Peters Methodist Church\nAllison Road\nBrislington",
            location=Point(-2.5417780465622686, 51.440043287399604),
            council_id="BST",
        )
        ps.elections = [timezone.now().date()]
        return ps

    def get_context_data(self, **kwargs):
        self.postcode = Postcode(
            "EXAMPLE"
        )  # put this in the logs so it is easy to exclude
        context = super().get_context_data(**kwargs)
        context["postcode"] = "BS4 4NL"  # show this on the page
        context["has_election"] = True
        context["election_explainers"] = []
        context["error"] = None
        context["custom"] = None
        context["requires_voter_id"] = True
        return context


class WeDontKnowView(PostcodeView):
    def get(self, request, *args, **kwargs):
        self.postcode = Postcode(kwargs["postcode"])
        rh = RoutingHelper(self.postcode)
        if rh.councils:
            return HttpResponseRedirect(
                reverse(
                    "multiple_councils_view",
                    kwargs={"postcode": self.postcode.without_space},
                )
            )
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def get_station(self):
        return None


class MultipleCouncilsView(TemplateView, LogLookUpMixin, LanguageMixin):
    """
    Because sometimes "we don't know" just isn't uncertain enough
    User should end up here when directed to WeDontKnow but when we
    there are uprns in multiple councils for their postcode.
    """

    template_name = "multiple_councils.html"

    def get(self, request, *args, **kwargs):
        self.postcode = Postcode(self.kwargs["postcode"])
        rh = RoutingHelper(self.postcode)

        if not rh.councils:
            return HttpResponseRedirect(rh.get_canonical_url(request))

        self.council_ids = rh.councils
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def get_context_data(self, **context):
        context["councils"] = Council.objects.filter(council_id__in=self.council_ids)
        context["territory"] = self.postcode.territory

        log_data = {
            "we_know_where_you_should_vote": False,
            "location": None,
            "council": None,
        }
        self.log_postcode(self.postcode, log_data, type(self).__name__)

        return context


class AddressFormView(FormView):
    form_class = AddressSelectForm
    template_name = "address_select.html"
    NOTINLIST = "519RA5LCGuHHXQvBUVgOXiCcqWy7SZG1inRDKcx1"

    def get_context_data(self, **kwargs):
        context = super(AddressFormView, self).get_context_data(**kwargs)
        context["noindex"] = True
        return context

    def get_form(self, form_class=AddressSelectForm):
        self.postcode = Postcode(self.kwargs["postcode"])

        addresses = Address.objects.filter(
            postcode=self.postcode.with_space
        ).select_related("uprntocouncil")

        if not addresses:
            raise Http404

        addresses_with_station = addresses.exclude(uprntocouncil__polling_station_id="")
        addresses_without_station = addresses.filter(
            uprntocouncil__polling_station_id=""
        )

        addresses_with_station = (
            AddressSorter(addresses_with_station).natural_sort()
            if addresses_with_station
            else []
        )
        addresses_without_station = (
            AddressSorter(addresses_without_station).natural_sort()
            if addresses_without_station
            else []
        )

        addresses = addresses_with_station + addresses_without_station

        select_addresses = [(element.uprn, element.address) for element in addresses]
        select_addresses.append((self.NOTINLIST, "My address is not in the list"))
        return form_class(
            select_addresses, self.postcode.without_space, **self.get_form_kwargs()
        )

    def form_valid(self, form):
        uprn = form.cleaned_data["address"]
        if uprn == self.NOTINLIST:
            self.success_url = reverse(
                "we_dont_know", kwargs={"postcode": self.postcode.without_space}
            )
        else:
            self.success_url = reverse("address_view", kwargs={"uprn": uprn})
        return super(AddressFormView, self).form_valid(form)
