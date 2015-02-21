from django.contrib.gis import admin

import models

class PollingStationAdmin(admin.OSMGeoAdmin):
    pass

class PollingDistrictAdmin(admin.OSMGeoAdmin):
    pass


admin.site.register(models.PollingStation, PollingStationAdmin)
admin.site.register(models.PollingDistrict, PollingDistrictAdmin)
