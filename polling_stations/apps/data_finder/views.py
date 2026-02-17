import abc
from datetime import datetime
from typing import Optional
from django.utils.safestring import mark_safe

from addressbase.models import Address
from api.councils import tmp_fix_parl_24_scotland_details
from councils.models import Council
from django.conf import settings
from django.contrib import messages
from django.contrib.gis.geos import Point
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils import timezone, translation
from django.utils.translation import gettext_lazy as _
from django.views.generic import FormView, TemplateView
from pollingstations.models import (
    AccessibilityInformation,
    PollingStation,
)
from uk_geo_utils.helpers import AddressSorter, Postcode

from polling_stations.settings.constants.importers import EONIImportScheme
from whitelabel.views import WhiteLabelTemplateOverrideMixin

from .forms import AddressSelectForm, PostcodeLookupForm
from .helpers import (
    DirectionsHelper,
    PostcodeError,
    RoutingHelper,
    geocode,
    get_council,
)
from .helpers.baked_data_helper import LocalParquetElectionsHelper
from .helpers.every_election import EEFetcher, EEWrapper, EmptyEEWrapper
from urllib.parse import urlencode


def reverse_with_qs(view, kwargs, request):
    """Returns a URL to route to, preserving any important query parameters"""
    _query_params_to_preserve = {
        "utm_content",
        "utm_medium",
        "utm_source",
        "utm_campaign",
    }
    url = reverse(view, kwargs=kwargs)
    query = urlencode(
        [
            (k, request.GET.getlist(k))
            for k in request.GET
            if k in _query_params_to_preserve
        ],
        doseq=True,
    )
    if query:
        url += "?" + query
    return url


def namespace_view(namespace, view):
    return f"{namespace}{view}"


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
    def log_postcode(self, postcode, context):
        # Log to firehose
        utm_data = {}

        if hasattr(self.request, "session"):
            utm_data = self.request.session.get("utm_data")

        entry = settings.POSTCODE_LOGGER.entry_class(
            postcode=postcode,
            dc_product=settings.POSTCODE_LOGGER.dc_product.wdiv,
            had_election=context.get("has_election", False),
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
    namespace = ""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["submit_url"] = reverse(namespace_view(self.namespace, "home"))

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
        self.success_url = reverse(
            namespace_view(self.namespace, rh.view), kwargs=rh.kwargs
        )

        return super(HomeView, self).form_valid(form)

    def form_invalid(self, form):
        context = self.get_context_data(form=form)
        context["postcode"] = form.data.get("postcode", "")
        return self.render_to_response(context)


class BasePollingStationView(
    TemplateView, LogLookUpMixin, LanguageMixin, metaclass=abc.ABCMeta
):
    template_name = "postcode_view.html"
    namespace = ""

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
            return EmptyEEWrapper()
        if rh.elections_response:
            return EEWrapper(
                rh.elections_response["ballots"],
                request_success=rh.elections_response["request_success"],
            )
        if not self.location or self.location.tuple == (0.0, 0.0):
            return EEWrapper(**EEFetcher(postcode=self.postcode).fetch())
        return EEWrapper(**EEFetcher(point=self.location).fetch())

    def get_directions(self):
        if self.location and self.station and self.station.location:
            dh = DirectionsHelper()
            return dh.get_directions(
                start_location=self.location, end_location=self.station.location
            )
        return None

    def we_know_where_you_should_vote(self):
        return polling_station_current(self.get_station())

    def get_ni_elected_rep_type(self):
        if settings.EONI_IMPORT_SCHEME == EONIImportScheme.LOCAL:
            return _("local Councillor")
        return _("Member of the Legislative Assembly, and Member of Parliament")

    def show_map(self, context):
        station = context.get("station")
        station_location = getattr(station, "location", None)
        advance_voting_station = context.get("advance_voting_station")
        advance_voting_station_location = getattr(
            advance_voting_station, "location", None
        )
        we_know_where_you_should_vote = context.get("we_know_where_you_should_vote")
        errors = context.get("errors")
        has_election = context.get("has_election")
        ni_out_of_cycle_station = context.get("ni_out_of_cycle_station")

        # If there are any errors return false
        if errors:
            return False

        # If we have a station location, are in Northern Ireland and there are no upcoming elections return true
        if ni_out_of_cycle_station and station_location:
            return True

        # If we have a station location or advance station location, and there are upcoming elections return true
        if (
            we_know_where_you_should_vote
            and (station_location or advance_voting_station_location)
            and has_election
        ):
            return True

        # Otherwise return false
        return False

    def get_context_data(self, **context):
        context["tile_layer"] = settings.TILE_LAYER
        context["mq_key"] = settings.MQ_KEY

        try:
            loc = self.get_location()
        except PostcodeError as e:
            context["error"] = str(e)
            context["postcode_form"] = PostcodeLookupForm({"postcode": self.postcode})
            context["postcode_form"].add_error("postcode", "Enter a valid postcode.")
            context["submit_url"] = reverse(namespace_view(self.namespace, "home"))
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
        next_election_date = ee.get_next_election_date()
        context["next_election_date"] = (
            datetime.strptime(next_election_date, "%Y-%m-%d").date()
            if next_election_date
            else None
        )
        context["multiple_elections"] = ee.multiple_elections
        context["election_explainers"] = ee.get_explanations()
        context["cancelled_election"] = ee.get_cancelled_election_info()
        context["advance_voting_station"] = self.get_advance_voting_station()
        context["requires_voter_id"] = ee.get_voter_id_status()
        context["has_city_of_london_ballots"] = ee.has_city_of_london_ballots

        context["postcode"] = self.postcode.with_space
        context["location"] = self.location
        context["council"] = self.council
        context["council"] = tmp_fix_parl_24_scotland_details(context["council"], ee)
        context["station"] = self.station
        context["directions"] = self.directions
        context["we_know_where_you_should_vote"] = self.we_know_where_you_should_vote()
        context["noindex"] = True
        context["territory"] = self.postcode.territory
        context["ni_out_of_cycle_station"] = False

        if (
            context["territory"] == "NI"
            and getattr(settings, "SHOW_EONI_STATIONS_ALL_THE_TIME", None)
            and self.station
            and not context["has_election"]
        ):
            context["ni_out_of_cycle_station"] = True
            context["ni_elected_rep_type"] = self.get_ni_elected_rep_type()

        context["show_map"] = self.show_map(context)

        self.log_postcode(self.postcode, context)
        return context


class PostcodeView(BasePollingStationView):
    def get(self, request, *args, **kwargs):
        if "postcode" in request.GET:
            self.kwargs["postcode"] = kwargs["postcode"] = request.GET["postcode"]
        if "postcode" not in kwargs or kwargs["postcode"] == "":
            return HttpResponseRedirect(reverse(namespace_view(self.namespace, "home")))

        rh = RoutingHelper(self.kwargs["postcode"])
        kwargs["rh"] = rh

        if rh.view != "postcode_view":
            return HttpResponseRedirect(
                reverse_with_qs(
                    namespace_view(self.namespace, rh.view), rh.kwargs, request
                )
            )

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
        if getattr(settings, "USE_LOCAL_PARQUET_ELECTIONS", False):
            helper = LocalParquetElectionsHelper()
            resp = helper.get_response(
                Postcode(self.address.postcode), self.address.uprn
            )
            return EEWrapper(
                resp["ballots"],
                request_success=resp["request_success"],
            )

        return EEWrapper(**EEFetcher(point=self.address.location).fetch())


class ExamplePostcodeView(BasePollingStationView):
    """
    This class presents a hard-coded example of what our website does
    without having to worry about having any data imported
    or whether an election is actually happening or not
    """

    def get(self, request, *args, **kwargs):
        kwargs["rh"] = RoutingHelper("BS4 4NL")
        context = self.get_context_data(**kwargs)
        url = reverse(namespace_view(self.namespace, "home"))
        message = mark_safe(
            f'THIS IS AN EXAMPLE PAGE. To find your polling station please return to the <a href="{url}">homepage</a> and enter your postcode.'
        )
        messages.error(self.request, message)
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
        context["requires_voter_id"] = True
        context["noindex"] = True
        context["show_map"] = True
        return context


class WeDontKnowView(PostcodeView):
    def get(self, request, *args, **kwargs):
        self.postcode = Postcode(kwargs["postcode"])
        rh = RoutingHelper(self.postcode)
        if rh.councils:
            return HttpResponseRedirect(
                reverse(
                    namespace_view(self.namespace, "multiple_councils_view"),
                    kwargs={"postcode": self.postcode.without_space},
                )
            )
        kwargs["rh"] = rh
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
    namespace = ""

    def get(self, request, *args, **kwargs):
        self.postcode = Postcode(self.kwargs["postcode"])
        rh = RoutingHelper(self.postcode)

        if not rh.councils:
            return HttpResponseRedirect(
                reverse_with_qs(
                    namespace_view(self.namespace, rh.view), rh.kwargs, request
                )
            )

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
        self.log_postcode(self.postcode, log_data)

        return context


class AddressFormView(FormView):
    form_class = AddressSelectForm
    template_name = "address_select.html"
    NOTINLIST = "519RA5LCGuHHXQvBUVgOXiCcqWy7SZG1inRDKcx1"
    namespace = ""

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

        """
        Note: There's some history here.
        We did try sorting addresses with a station assigned ahead
        of addresses without a station assigned. See
        https://github.com/DemocracyClub/UK-Polling-Stations/commit/61d2908ddab15c24ccd0b644fba86d413752438f

        This works well if all the addresses without a station
        assigned are pubs, shops, etc
        However, if you have a lot of numbered streets where a handful of
        numbered houses are not assigned to a station this leads to address
        pickers that are sorted in an incomprehensible way.
        """
        sorter = AddressSorter(addresses)
        addresses = sorter.natural_sort()

        select_addresses = [(element.uprn, element.address) for element in addresses]
        if self.NOTINLIST:
            select_addresses.append((self.NOTINLIST, "My address is not in the list"))
        return form_class(
            select_addresses, self.postcode.without_space, **self.get_form_kwargs()
        )

    def form_valid(self, form):
        uprn = form.cleaned_data["address"]
        if uprn == self.NOTINLIST:
            self.success_url = reverse(
                namespace_view(self.namespace, "we_dont_know"),
                kwargs={"postcode": self.postcode.without_space},
            )
        else:
            self.success_url = reverse(
                namespace_view(self.namespace, "address_view"), kwargs={"uprn": uprn}
            )
        return super(AddressFormView, self).form_valid(form)
