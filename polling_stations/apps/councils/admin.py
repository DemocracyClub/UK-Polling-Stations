from django.contrib.gis import admin
from django import forms

from data_finder.admin import ReadOnlyAdminMixIn
from data_finder.models import DataQuality

import models

class CouncilDataInfoInline(admin.StackedInline):
    model = DataQuality
    def has_delete_permission(self, request, obj=None):
            return False

class CouncilAdmin(ReadOnlyAdminMixIn, admin.OSMGeoAdmin):
    modifiable = False
    exclude_from_read_only = [
        'area',
        'location',
    ]
    inlines = [CouncilDataInfoInline, ]

admin.site.register(models.Council, CouncilAdmin)

