from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter
from pollingstations.models import PollingStation
from addressbase.models import Address


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "FLN"
    addresses_name = "2026-05-07/2026-02-27T11:02:16.435939/Democracy_Club__07May2026 - Flintshire.CSV"
    stations_name = "2026-05-07/2026-02-27T11:02:16.435939/Democracy_Club__07May2026 - Flintshire.CSV"
    elections = ["2026-05-07"]
    csv_encoding = "windows-1252"

    def station_record_to_dict(self, record):
        # The postcodes of the following stations have been confirmed by the council:

        # Village Hall/Neuadd Y Pentref, Rhesycae/Rhes-y-Cae, Nr Holywell/Nr Treffynnon, CH8 8JR
        # Community Centre/Canolfan Gymunedol, Mynydd Isa, Mold/Yr Wyddgrug, CH7 6UH

        # Postcode changes confirmed by council:
        # Village Hall/Neuadd Y Pentref, Ysceifiog, Nr Holywell/Nr Treffynnon, CH8 8NR
        if record.polling_place_id == "8249":
            record = record._replace(polling_place_postcode="CH8 8NJ")

        # Rhosesmor Village Hall, Neuadd Bentref Rhosesmor, Rhosesmor, Mold/Yr Wyddgrug, CH7 6PQ
        if record.polling_place_id == "8237":
            record = record._replace(polling_place_postcode="CH7 6WF")

        # St. Michael`s Church/Eglwys Sant Mihangel, Brynford/Brynffordd, CH8 8AD
        if record.polling_place_id == "8223":
            record = record._replace(polling_place_postcode="CH8 8LQ")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10090462571",  # PLYMOUTH COPSE, BABELL, HOLYWELL
            "10013705239",  # DYFFRYN AUR, BABELL, HOLYWELL
            "10013716952",  # NANT Y FUWCH, PENTRE HALKYN, HOLYWELL
            "10013694502",  # HOLLY COTTAGE, WINDMILL, PENTRE HALKYN, HOLYWELL
            "10013694267",  # 3 MOEL VIEW, WERN ROAD, RHOSESMOR, MOLD
            "10013695024",  # 1 MOEL VIEW, WERN ROAD, RHOSESMOR, MOLD
            "10023845151",  # 2 MOEL VIEW, WERN ROAD, RHOSESMOR, MOLD
            "10013707528",  # BROOKLANDS, FFRITH, WREXHAM
            "100100930264",  # THE GRANGE, SANDY LANE, HIGHER KINNERTON, CHESTER
            "200002940307",  # GRANGE FARM COTTAGE, SANDY LANE, HIGHER KINNERTON, CHESTER
            "100100219238",  # 86 SANDY LANE, HIGHER KINNERTON, CHESTER
            "100100209552",  # WOODVILLE, HIGH STREET, BAGILLT
            "10023843516",  # ELM HOUSE, HIGH STREET, BAGILLT
            "200002942099",  # FLAT 2 WELL STREET, HOLYWELL
            "10093285045",  # 11A CHESTER ROAD WEST, SHOTTON, DEESIDE
        ]:
            return None
        if record.addressline6 in [
            # split
            "CH7 6BA",
            "CH8 7ED",
            "CH7 6SD",
            "CH8 7PQ",
            "CH6 5TG",
            "CH8 8NY",
            "CH4 0PE",
            "CH5 3EF",
            "CH7 2JR",
            "CH8 8NF",
            "CH8 8LR",
            "CH8 8JY",
            "CH5 1QR",
            "CH7 6YX",
            "CH6 5TP",
            "CH7 6AH",
            "LL12 9DU",
            "CH5 1PD",
            "LL12 9HN",
            "CH7 6EH",
            "CH7 6PA",
            "CH7 2JP",
            # suspect
            "CH8 7AX",
            "CH8 7EY",
            "CH6 6ES",
            "CH5 4XL",
            "CH4 0QN",
        ]:
            return None
        return super().address_record_to_dict(record)

    def post_import(self):
        # The a117 data the councils sent had UPRNs for polling stations that weren't in the EMS data
        a11y_uprns = {
            "8227": 10023845867,
            "8264": 100101033883,
            "8268": 10013711624,
            "8271": 100101033926,
            "8275": 10023847579,
            "8279": 10093286971,
            "8290": 10023844996,
            "8292": 10023846086,
            "8295": 10013699946,
            "8303": 10023847499,
            "8307": 10023845259,
            "8311": 10023844173,
            "8315": 10090461134,
            "8319": 10090461492,
            "8323": 10023846735,
            "8327": 10013700983,
            "8331": 10023846948,
            "8335": 10090461394,
            "8342": 10095362450,
            "8346": 10013696154,
            "8349": 10090462862,
            "8353": 10023845942,
            "8357": 200002941840,
            "8361": 10023845871,
            "8365": 10023845866,
            "8369": 10013703522,
            "8373": 10023846265,
            "8377": 100101033076,
            "8385": 10013694653,
            "8391": 10023846004,
            "8393": 100100932844,
            "8395": 200002941454,
            "8398": 10095364861,
            "8402": 200002941448,
            "8406": 10013712008,
            "8413": 200002941469,
            "8417": 10095362618,
            "8420": 10093286963,
            "8427": 10013707349,
            "8430": 100101033525,
            "8434": 10093286964,
            "8438": 10023845884,
            "8442": 100101033677,
            "8450": 100100931741,
            "8451": 10013698260,
            "8455": 10013708063,
            "8457": 10013697800,
            "8460": 10023845796,
            "8462": 10013697305,
            "8466": 10090462978,
            "8474": 10023845821,
            "8477": 10023846085,
            "8479": 100101033354,
            "8483": 100100931289,
            "8486": 100100931319,
            "8489": 200002940746,
            "8493": 100101033528,
            "8497": 10093286972,
            "8501": 100100930269,
            "8505": 10013703372,
            "8509": 10023845978,
            "8513": 10023847389,
            "8517": 10023845473,
            "8526": 100101033393,
            "8529": 100101033554,
            "8533": 200002940568,
            "8535": 100101033177,
            "8539": 10013706417,
            "8543": 100101033201,
            "8545": 10093286967,
            "8549": 10023845797,
            "8555": 10023845943,
            "8558": 10023846087,
            "8562": 10093287006,
            "8565": 100101034030,
            "8569": 10013702980,
            "8573": 10095364862,
            "8624": 10090462565,
            "8626": 200002940322,
            "8642": 200002940984,
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
