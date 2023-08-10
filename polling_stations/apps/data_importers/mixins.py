from typing import List

from addressbase.models import UprnToCouncil
from councils.models import Council
from data_importers.base_importers import BaseBaseImporter, BaseImporter
from pollingstations.models import AdvanceVotingStation
from rich.table import Table


def advance_voting_report(import_cls: "AdvanceVotingMixin", council: Council) -> Table:
    table = Table(title="Advance Voting stations", show_header=True, min_width=50)
    table.add_column("AVSs imported")
    table.add_column("UPRNs assigned")

    avs_qs = AdvanceVotingStation.objects.filter(
        uprntocouncil__lad=council.geography.gss
    ).distinct("pk")
    if avs_qs.exists():
        for avs in avs_qs:
            table.add_row(avs.name, str(avs.uprntocouncil_set.count()))
        if len(avs_qs) > 1:
            table.add_row(
                "TOTAL",
                str(sum([avs.uprntocouncil_set.count() for avs in avs_qs])),
                style="bold",
            )
    else:
        table.add_row("WARNING: No Advance stations imported")
    return table


class AdvanceVotingMixin(BaseBaseImporter):
    advance_stations = []

    def __init__(self):
        super().__init__()

        # Make sure users of this mixin are calling super()
        if self.__class__.post_import.__code__.co_freevars != ("__class__",):
            raise TypeError(
                "MUST Call super() in post_import when using AdvanceVotingMixin"
            )

    def get_extra_reports(self: BaseImporter):
        extra_reports: List = super().get_extra_reports()
        extra_reports.append(advance_voting_report)
        return extra_reports

    def add_advance_voting_stations(self):
        raise NotImplementedError(
            "add_advance_voting_stations when using `AdvanceVotingMixin`"
        )

    def post_import(self):
        super().post_import()
        self.add_advance_voting_stations()

    def teardown(self, council):
        super().teardown(council)
        UprnToCouncil.objects.filter(lad=council.geography.gss).update(
            advance_voting_station=None
        )
        AdvanceVotingStation.objects.filter(council=council).delete()
