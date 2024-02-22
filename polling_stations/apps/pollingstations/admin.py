from data_importers.event_helpers import record_set_station_visibility_event
from data_importers.event_types import EventUserType
from django.contrib import admin
from django.contrib.gis.db import models
from django.contrib.gis.forms import OSMWidget
from django.db import transaction
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
    list_filter = ["visibility", ("council", admin.RelatedOnlyFieldListFilter)]

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

    def get_fields(self, request, obj=None):
        fields = (
            "visibility",
            "council",
            "internal_council_id",
            "postcode",
            "address",
            "polling_district_id",
        )
        if obj.location:
            fields += ("location",)
        return fields

    def save_model(self, request, obj, form, change):
        if not change:
            return super().save_model(request, obj, form, change)
        # get election from latest import event
        if "visibility" in form.changed_data:
            record_set_station_visibility_event(
                obj,
                form.cleaned_data["visibility"],
                metadata={
                    "source": EventUserType.ADMIN,
                },
            )
        return super().save_model(request, obj, form, change)

    @admin.action(
        description="Unpublish selected Polling Stations. This will hide them from users."
    )
    @transaction.atomic
    def unpublish(self, request, queryset):
        queryset.update(visibility=VisibilityChoices.UNPUBLISHED)
        for station in queryset:
            record_set_station_visibility_event(
                station,
                VisibilityChoices.UNPUBLISHED,
                metadata={
                    "source": EventUserType.ADMIN,
                },
            )

    @admin.action(
        description="Republish selected Polling Stations. This will make them visible to users."
    )
    @transaction.atomic
    def publish(self, request, queryset):
        queryset.update(visibility=VisibilityChoices.PUBLISHED)
        for station in queryset:
            record_set_station_visibility_event(
                station,
                VisibilityChoices.PUBLISHED,
                metadata={
                    "source": EventUserType.ADMIN,
                },
            )

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
