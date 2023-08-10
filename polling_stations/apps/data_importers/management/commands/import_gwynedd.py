from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "GWN"
    addresses_name = (
        "2022-05-05/2022-04-14T08:51:48.064164/polling_station_export-2022-04-14.csv"
    )
    stations_name = (
        "2022-05-05/2022-04-14T08:51:48.064164/polling_station_export-2022-04-14.csv"
    )
    elections = ["2022-05-05"]
    csv_encoding = "windows-1252"

    # > WARNING: Polling station NEUADD BENTREF ABERANGELL (0-neuadd-bentref-aberangell)
    # > is in Powys County Council (POW) but target council is Gwynedd Council (GWN) -
    # > manual check recommended
    #
    # Checked; actual village hall is within Aberangell, on the right side of the
    # boundary.

    def station_record_to_dict(self, record):
        # TY'N LLAN - Gorsaf Newydd/New Polling Station, LLANDWROG, CAERNARFON
        if record.pollingstationnumber == "16":
            # https://tynllan.cymru/cysylltu-a-ni/
            record = record._replace(pollingstationpostcode="LL54 5SY")  # was LL54 4SY

        # CAPEL HOREB - Gorsaf Newydd/New Polling Station, RHOSTRYFAN, CAERNARFON, GWYNEDD
        if record.pollingstationnumber == "10":
            # Via UPRN 10070271330 (not necessarily the same building, but close enough)
            record = record._replace(pollingstationpostcode="LL54 7LT")  # was LL57 7LT

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        if record.housepostcode in [
            "LL57 4HG",
            "LL53 7TP",
            "LL55 2SG",
            "LL48 6AY",
            "LL23 7LE",
            "LL53 8NH",
            "LL54 7BN",
            "LL53 8PS",
            "LL54 7UB",
            "LL53 5TP",
            "LL55 4BT",
            "LL57 2NZ",
            "LL36 9LF",
            "LL55 4RR",
            "LL57 3YF",
            "LL53 5AG",
            "LL53 6SY",
            "LL57 3UA",
            "LL55 2TD",
            "LL53 8DR",
        ]:
            return None  # split

        if record.uprn in [
            "200003167346",  # 21 RALPH STREET, BORTH-Y-GEST, PORTHMADOG
            "100100020767",  # 16 LON CEREDIGION, PWLLHELI
            "200003162781",  # 6 CHURCH PLACE, PWLLHELI
            "200003166018",  # 5 HOLYWELL TERRACE, CRICCIETH
            "200003176318",  # 1 PRETORIA TERRACE, SARN, PWLLHELI
            "10024095703",  # PENRHYN LLYN, SARN, PWLLHELI
        ]:
            return None

        rec = super().address_record_to_dict(record)

        fix_stations = {
            "34-festri-capel-brynaerau-pontllyfni": "35-neuadd-bentref-clynnog-fawr",
            "35-neuadd-bentref-clynnog-fawr": "36-festri-capel-mc-pantglas",
            "36-festri-capel-mc-pantglas": "34-festri-capel-brynaerau-pontllyfni",
        }
        if rec and rec["polling_station_id"] in fix_stations:
            rec["polling_station_id"] = fix_stations[rec["polling_station_id"]]

        return rec
