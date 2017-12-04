from django.contrib.gis import admin

from . import models

class PollingStationAdmin(admin.OSMGeoAdmin):
    pass

class PollingDistrictAdmin(admin.OSMGeoAdmin):
    list_filter = ('council',)

class CustomFinderAdmin(admin.ModelAdmin):
    pass


admin.site.register(models.PollingStation, PollingStationAdmin)
admin.site.register(models.PollingDistrict, PollingDistrictAdmin)
admin.site.register(models.CustomFinder, CustomFinderAdmin)
