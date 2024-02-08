from django.contrib import admin
from django.contrib.gis.db import models
from django.contrib.gis.forms import OSMWidget
from pollingstations.models import PollingStation, VisibilityChoices


class PollingStationAdmin(admin.ModelAdmin):
    actions = ["unpublish", "publish"]

    search_fields = [
        "address",
        "postcode",
        "council__name",
        "council__council_id",
        "internal_council_id",
    ]

    # Filter on published status or council name
    list_filter = ["visibility", "council__name"]

    # Human-readable name for list view
    list_display = [
        "display_name",
        "council_name",
        "internal_council_id",
        "published_status",
    ]

    # We're making it readonly for now
    readonly_fields = [
        "council",
        "internal_council_id",
        "postcode",
        "address",
        "polling_district_id",
    ]
    # Make the map Uneditable
    modifiable = False
    # Use OSM basemap
    formfield_overrides = {models.PointField: {"widget": OSMWidget}}

    @admin.action(
        description="Unpublish selected Polling Stations. This will hide them from users."
    )
    def unpublish(self, request, queryset):
        queryset.update(visibility=VisibilityChoices.UNPUBLISHED)

    @admin.action(
        description="Republish selected Polling Stations. This will make them visible to users."
    )
    def publish(self, request, queryset):
        queryset.update(visibility=VisibilityChoices.PUBLISHED)

    @admin.display(description="Station Name")
    def display_name(self, obj):
        return obj.address.split("\n")[0]

    @admin.display(description="Council Name")
    def council_name(self, obj):
        return obj.council.name

    @admin.display(description="Published Status")
    def published_status(self, obj):
        return VisibilityChoices[obj.visibility].label

    # Disable add action
    def has_add_permission(self, request, obj=None):
        return False

    # Disable delete action
    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(PollingStation, PollingStationAdmin)
