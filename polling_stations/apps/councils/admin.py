from django.contrib.gis import admin

import models

class CouncilAdmin(admin.OSMGeoAdmin):
    pass

admin.site.register(models.Council, CouncilAdmin)

