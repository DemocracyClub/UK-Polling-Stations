from django.contrib.gis.geos import Point

from django.views.generic import FormView, DetailView

from councils.models import Council
from .forms import PostcodeLookupForm
from .helpers import geocode

class HomeView(FormView):
    form_class = PostcodeLookupForm
    template_name = "home.html"

    def form_valid(self, form):
        l = geocode(form.cleaned_data['postcode'])
        location = Point(l['wgs84_lon'], l['wgs84_lat'])


        council = Council.objects.get(area__covers=location)
        self.success_url = council.get_absolute_url()
        return super(HomeView, self).form_valid(form)

class CouncilView(DetailView):
    model = Council