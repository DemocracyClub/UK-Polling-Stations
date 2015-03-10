# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.views.generic import TemplateView

from data_finder.views import HomeView, CouncilView, PostcodeView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^league_table/', include('data_collection.urls')),

    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^council/(?P<pk>.+)/$', CouncilView.as_view(), name='council'),
    url(r'^postcode/(?P<postcode>.+)/$',
        PostcodeView.as_view(), name='postcode_view'),

) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

