from django.contrib.gis import admin

from . import models

class PollingStationAdmin(admin.OSMGeoAdmin):
    pass

class PollingDistrictAdmin(admin.OSMGeoAdmin):
    list_filter = ('council',)
    pass


admin.site.register(models.PollingStation, PollingStationAdmin)
admin.site.register(models.PollingDistrict, PollingDistrictAdmin)
