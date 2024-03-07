import django_filters
from councils.models import Council
from dc_utils.filter_widgets import DSLinkWidget
from django.db.models import Exists, OuterRef
from file_uploads.models import UploadStatusChoices
from pollingstations.models import PollingStation


class CouncilListUploadFilter(django_filters.FilterSet):
    class Meta:
        model = Council
        fields = [
            "name",
            "pollingstations",
            "upload",
        ]

    name = django_filters.CharFilter(label="Council Name", method="filter_name")
    pollingstations = django_filters.ChoiceFilter(
        method="filter_pollingstation",
        label="has stations",
        widget=DSLinkWidget(),
        choices=[
            (1, "With Stations"),
            (0, "Without Stations"),
        ],
    )
    upload = django_filters.ChoiceFilter(
        label="uploads",
        method="filter_upload",
        widget=DSLinkWidget(),
        choices=UploadStatusChoices.choices,
    )

    def filter_name(self, queryset, name, value):
        return queryset.filter(name__icontains=value)

    def filter_pollingstation(self, queryset, name, value):
        """
        Filter on whether stations have been imported
        """
        pollingstations = PollingStation.objects.filter(council_id=OuterRef("pk"))
        if value == "1":
            queryset = queryset.filter(Exists(pollingstations))
        if value == "0":
            queryset = queryset.filter(~Exists(pollingstations))
        return queryset

    def filter_upload(self, queryset, name, value):
        return queryset.filter(latest_upload_status=value)
