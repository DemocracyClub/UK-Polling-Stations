import abc

from django.conf import settings
from django.contrib.gis.geos import Point
from django.urls import reverse
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404
from django.views.generic import FormView, TemplateView
from django.utils import translation
from uk_geo_utils.geocoders import MultipleCodesException

from addressbase.models import Address
from councils.models import Council
from data_finder.models import LoggedPostcode
from pollingstations.models import PollingStation, CustomFinder
from uk_geo_utils.helpers import AddressSorter, Postcode
from whitelabel.views import WhiteLabelTemplateOverrideMixin
from .forms import PostcodeLookupForm, AddressSelectForm
from .helpers import (
    DirectionsHelper,
    get_council,
    geocode,
    EveryElectionWrapper,
    PostcodeError,
    RoutingHelper,
)


class LogLookUpMixin(object):
    def log_postcode(self, postcode, context, view_used):

        if "language" in context:
            language = context["language"]
        else:
            language = self.get_language()

        if "brand" in context:
            brand = context["brand"]
        else:
            brand = self.request.brand

        if "has_election" in context:
            has_election = context["has_election"]
        else:
            has_election = None

        kwargs = {
            "postcode": postcode.without_space,
            "had_data": bool(context["we_know_where_you_should_vote"]),
            "location": context["location"],
            "council": context["council"],
            "brand": brand,
            "language": language,
            "view_used": view_used,
            "has_election": has_election,
        }
        if "api_user" in context:
            kwargs["api_user"] = context["api_user"]
        kwargs.update(
            {k: v[0:100] for k, v in self.request.session["utm_data"].items()}
        )
        LoggedPostcode.objects.create(**kwargs)


class LanguageMixin(object):
    def get_language(self):
        if (
            self.request.session
            and translation.LANGUAGE_SESSION_KEY in self.request.session
            and self.request.session[translation.LANGUAGE_SESSION_KEY]
        ):
            return self.request.session[translation.LANGUAGE_SESSION_KEY]
        else:
            return ""


class HomeView(WhiteLabelTemplateOverrideMixin, FormView):
    form_class = PostcodeLookupForm
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        """
        TODO: revisit idea of polling day-specific content
        https://github.com/DemocracyClub/UK-Polling-Stations/pull/2037/files#diff-78a9fc588889ef751c68b530b1af1e80
        https://github.com/DemocracyClub/UK-Polling-Stations/issues/2051
        """
        context["show_polls_open"] = False
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

    def get_ee_wrapper(self):
        return EveryElectionWrapper(postcode=self.postcode)

    def get_directions(self):
        if self.location and self.station and self.station.location:
            dh = DirectionsHelper()
            return dh.get_directions(
                start_location=self.location, end_location=self.station.location
            )
        else:
            return None

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
        self.directions = self.get_directions()

        ee = self.get_ee_wrapper()
        context["has_election"] = ee.has_election()
        context["election_explainers"] = ee.get_explanations()
        context["cancelled_election"] = ee.get_cancelled_election_info()
        context["voter_id_pilot"] = ee.get_id_pilot_info()

        context["postcode"] = self.postcode.with_space
        context["location"] = self.location
        context["council"] = self.council
        context["station"] = self.station
        context["directions"] = self.directions
        context["we_know_where_you_should_vote"] = self.station
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

        if rh.view != "postcode_view":
            return HttpResponseRedirect(rh.get_canonical_url(request))
        else:
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
        return None


class AddressView(BasePollingStationView):
    def get(self, request, *args, **kwargs):
        self.address = get_object_or_404(Address, uprn=self.kwargs["uprn"])
        self.postcode = Postcode(self.address.postcode)
        context = self.get_context_data(**kwargs)

        return self.render_to_response(context)

    def get_location(self):
        return geocode(self.postcode)

    def get_council(self, geocode_result):
        return self.address.council

    def get_station(self):
        return self.address.polling_station

    def get_ee_wrapper(self):
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
        return PollingStation(
            internal_council_id="BREF",
            postcode="BS4 4NZ",
            address="St Peters Methodist Church\nAllison Road\nBrislington",
            location=Point(-2.5417780465622686, 51.440043287399604),
            council_id="BST",
        )

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
        else:
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

        addresses = Address.objects.filter(postcode=self.postcode.with_space)

        if not addresses:
            raise Http404

        sorter = AddressSorter(addresses)
        addresses = sorter.natural_sort()
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
