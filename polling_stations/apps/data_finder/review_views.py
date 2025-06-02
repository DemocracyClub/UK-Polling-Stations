import data_finder.views as data_finder_views
from django.shortcuts import get_object_or_404
from addressbase.models import Address
from django.urls import reverse
from django.http import HttpResponseRedirect


class HomeView(data_finder_views.HomeView):
    template_name = "reviews/WLL/20250609/home.html"
    namespace = "reviews:"


class PostcodeView(data_finder_views.PostcodeView):
    template_name = "reviews/WLL/20250609/postcode_view.html"
    namespace = "reviews:"

    def get(self, request, *args, **kwargs):
        resp = super().get(request, *args, **kwargs)
        council = getattr(self, "council", None)
        if council and council.council_id != "WLL":
            return HttpResponseRedirect(reverse("postcode_view", kwargs=kwargs))
        return resp

    def we_know_where_you_should_vote(self):
        return self.get_station()

    def get_ee_wrapper(self, *args, **kwargs):
        ee = super().get_ee_wrapper(*args, **kwargs)
        ee.has_election = lambda: True
        return ee


class AddressView(data_finder_views.AddressView):
    template_name = "reviews/WLL/20250609/postcode_view.html"
    namespace = "reviews:"

    def get(self, request, *args, **kwargs):
        address = get_object_or_404(
            Address.objects.select_related("uprntocouncil"), uprn=self.kwargs["uprn"]
        )
        if address.uprntocouncil.lad != "E08000030":
            return HttpResponseRedirect(reverse("address_view", kwargs=kwargs))
        return super().get(request, *args, **kwargs)

    def we_know_where_you_should_vote(self):
        return self.get_station()

    def get_ee_wrapper(self, *args, **kwargs):
        ee = super().get_ee_wrapper(*args, **kwargs)
        ee.has_election = lambda: True
        return ee


class WeDontKnowView(data_finder_views.WeDontKnowView):
    template_name = "reviews/WLL/20250609/postcode_view.html"
    namespace = "reviews:"

    def get(self, request, *args, **kwargs):
        resp = super().get(request, *args, **kwargs)
        council = getattr(self, "council", None)
        if council and council.council_id != "WLL":
            return HttpResponseRedirect(reverse("we_dont_know", kwargs=kwargs))
        return resp


class AddressFormView(data_finder_views.AddressFormView):
    namespace = "reviews:"
    NOTINLIST = ""  # disable "My address is not in the list" option
