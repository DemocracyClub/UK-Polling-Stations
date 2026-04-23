from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter
from pollingstations.models import PollingStation
from addressbase.models import Address


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "CWY"
    addresses_name = (
        "2026-05-07/2026-02-23T09:57:03.243783/Democracy_Club__07May2026 (2).tsv"
    )
    stations_name = (
        "2026-05-07/2026-02-23T09:57:03.243783/Democracy_Club__07May2026 (2).tsv"
    )
    elections = ["2026-05-07"]
    csv_encoding = "windows-1252"
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        if record.property_urn.lstrip(" 0") in [
            "50000011090",  # THE LIGHTHOUSE, MARINE DRIVE, LLANDUDNO
            "200002948867",  # THE LILLY, WEST PARADE, LLANDUDNO
            "10094422154",  # WEST VIEW, WEST PARADE, LLANDUDNO
            "100100430017",  # 91 LLANDUDNO ROAD, PENRHYN BAY, LLANDUDNO
            "100100441132",  # 20 CAMBRIA ROAD, OLD COLWYN, COLWYN BAY
            "50000016206",  # FLAT 1 REGENT HOUSE BRIDGE STREET, ABERGELE
            "10091011054",  # FLAT 2 REGENT HOUSE BRIDGE STREET, ABERGELE
            "10035304364",  # PLAS ISAF, GROESFFORDD MARLI, ABERGELE
            "10024205839",  # ALLTWEN, NANT BWLCH YR HAIARN, TREFRIW
            "10024205527",  # BUARTH FARM, ROWEN, CONWY
            "10024340201",  # HEN STABL, PLAS UCHA, LLANRWST
            "50000019771",  # SIAMBRWEN, BETWS ROAD, LLANRWST
            "10091007935",  # ABATY HEN COLWYN, ABERGELE ROAD, OLD COLWYN, COLWYN BAY
        ]:
            return None

        if record.addressline6 in [
            # splits
            "LL32 8HW",
            "LL22 7DT",
            "LL30 1YQ",
            "LL24 0LP",
            "LL30 1NT",
            "LL31 9EQ",
            "LL26 0YU",
            "LL21 9PH",
            "LL28 4AN",
            # suspect
            "LL22 8FB",
            "LL30 2DB",
            "LL34 6AQ",
        ]:
            return None

        return super().address_record_to_dict(record)

    def post_import(self):
        # The a117 data the councils sent had UPRNs for polling stations that weren't in the EMS data
        a11y_uprns = {
            "10322": 10024340906,
            "10329": 10091007039,
            "10332": 10091006937,
            "10335": 10024206861,
            "10342": 10035305216,
            "10346": 10023741525,
            "10349": 10024342954,
            "10352": 10024341057,
            "10356": 50000001676,
            "10359": 10091010567,
            "10362": 10091006960,
            "10365": 10024342200,
            "10369": 10024340711,
            "10372": 50000007859,
            "10375": 10024341078,
            "10378": 10024339891,
            "10381": 10091010575,
            "10385": 10024341082,
            "10389": 10024340542,
            "10392": 200001866568,
            "10395": 10024340643,
            "10398": 200002948909,
            "10401": 10024340733,
            "10405": 10024340563,
            "10409": 10024340477,
            "10412": 10091010568,
            "10415": 200001866318,
            "10418": 10024340644,
            "10420": 10024340974,
            "10423": 10023740030,
            "10427": 50000008916,
            "10431": 10024339580,
            "10435": 10024339845,
            "10438": 10024339561,
            "10441": 10024342715,
            "10444": 10024342180,
            "10448": 10024339827,
            "10451": 10024343579,
            "10454": 10024339867,
            "10463": 10091010576,
            "10467": 10024340835,
            "10470": 10091010577,
            "10474": 10024341066,
            "10478": 10024340670,
            "10481": 10024340749,
            "10484": 10024340793,
            "10487": 10091010570,
            "10491": 10091010566,
            "10495": 10024342961,
            "10498": 10024342719,
            "10501": 50000004480,
            "10505": 200002947990,
            "10508": 10035043947,
            "10511": 100100952785,
            "10514": 50000007375,
            "10518": 50000021676,
            "10521": 10024343472,
            "10525": 50000009047,
            "10528": 10091007820,
            "10530": 200002948547,
            "10534": 50000009101,
            "10537": 100101036865,
            "10541": 10035305633,
            "10544": 10024342765,
            "10548": 100101036616,
            "10552": 10024341034,
            "10556": 200001762051,
            "10559": 10023740068,
            "10563": 10035305011,
            "10570": 10024341047,
            "10573": 200002946532,
            "10577": 200002946508,
        }

        for station_id, uprn in a11y_uprns.items():
            try:
                ps = PollingStation.objects.get(internal_council_id=station_id)
                if not ps.location:
                    address = Address.objects.get(uprn=uprn)
                    ps.location = address.location
                    ps.save()
            except (PollingStation.DoesNotExist, Address.DoesNotExist):
                continue
