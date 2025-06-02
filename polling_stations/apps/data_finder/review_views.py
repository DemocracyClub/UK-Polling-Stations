import data_finder.views as data_finder_views
from django.urls import reverse
from django.http import HttpResponseRedirect
from .forms import PostcodeLookupForm
from .views import namespace_view


class HomeView(data_finder_views.HomeView):
    template_name = "reviews/WLL/20250609/home.html"
    namespace = "reviews:"


class PostcodeView(data_finder_views.PostcodeView):
    template_name = "reviews/WLL/20250609/postcode_view.html"
    namespace = "reviews:"

    def get_context_data(self, **context):
        context = super().get_context_data(**context)
        postcode = context["postcode"]
        if context.get("council") and context["council"].council_id != "WLL":
            context = {
                "error": "postcode_outside_walsall",
                "postcode_form": PostcodeLookupForm({"postcode": self.postcode}),
                "postcode": postcode,
                "submit_url": reverse(namespace_view(self.namespace, "home")),
            }
            context["postcode_form"].add_error(
                "postcode", "Enter a postcode in Walsall Council"
            )
        return context

    def we_know_where_you_should_vote(self):
        return self.get_station()

    def get_ee_wrapper(self, *args, **kwargs):
        ee = super().get_ee_wrapper(*args, **kwargs)
        ee.has_election = lambda: True
        return ee


class AddressView(data_finder_views.AddressView):
    template_name = "reviews/WLL/20250609/postcode_view.html"
    namespace = "reviews:"

    def get_context_data(self, **context):
        context = super().get_context_data(**context)
        postcode = context["postcode"]
        if context.get("council") and context["council"].council_id != "WLL":
            context = {
                "error": "address_outside_walsall",
                "postcode": postcode,
                "submit_url": reverse(namespace_view(self.namespace, "home")),
            }
        return context

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
