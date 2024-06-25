from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "GWN"
    addresses_name = "2024-07-04/2024-06-25T12:51:22.888148/GWN_combined.csv"
    stations_name = "2024-07-04/2024-06-25T12:51:22.888148/GWN_combined.csv"
    elections = ["2024-07-04"]
    csv_encoding = "windows-1252"

    # > WARNING: Polling station NEUADD BENTREF ABERANGELL (134-neuadd-bentref-aberangell)
    # > is in Powys County Council (POW) but target council is Gwynedd Council (GWN) -
    # > manual check recommended
    #
    # Checked; actual village hall is within Aberangell, on the right side of the
    # boundary.

    def station_record_to_dict(self, record):
        # CAPEL HOREB - Gorsaf Newydd/New Polling Station, RHOSTRYFAN, CAERNARFON, GWYNEDD
        if self.get_station_hash(record) == "22-capel-horeb":
            # Via UPRN 10070271330 (not necessarily the same building, but close enough)
            record = record._replace(pollingstationpostcode="LL54 7LT")  # was LL57 7LT

        # postcode different from addressbase: CANOLFAN EDERN, EDERN, LL53 8YU
        if self.get_station_hash(record) == "84-canolfan-edern":
            record = record._replace(pollingstationpostcode="")  # addressbase: LL53 8YS

        # postcode different from addresbase: CANOLFAN GYMDEITHASOL LLANFROTHEN, LLANFROTHEN, LL48 6LJ
        if self.get_station_hash(record) == "114-canolfan-gymdeithasol-llanfrothen":
            record = record._replace(pollingstationpostcode="")  # addressbase: LL48 6BQ

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "200003162781",  # 6 CHURCH PLACE, PWLLHELI
            "200003166018",  # 5 HOLYWELL TERRACE, CRICCIETH
            "200003195096",  # 8 PEN Y GRAIG, BETHESDA, BANGOR
            "200003163977",  # 19 VICTORIA ROAD, PENYGROES, CAERNARFON
            "200003165113",  # 4 POOL HILL, CAERNARFON
            "10090569131",  # FLAT 21 POOL STREET, CAERNARFON
            "200003164854",  # 23 POOL HILL, CAERNARFON
            "200003164853",  # 21 POOL HILL, CAERNARFON
            "10070361201",  # TY CAM, RHOSTRYFAN, CAERNARFON
            "200003178611",  # COED MAWR COTTAGE, LLANBERIS ROAD, RHOSBODRUAL, CAERNARFON
            "200003178515",  # 27 LLANBERIS ROAD, RHOSBODRUAL, CAERNARFON
            "10094363547",  # 47 PLAS Y COED, BANGOR
        ]:
            return None

        if record.housepostcode in [
            # splits
            "LL53 7TP",
            "LL53 5AG",
            "LL53 6SY",
            "LL53 8DR",
            "LL54 7UB",
            "LL48 6AY",
            "LL53 5TP",
            "LL55 2TD",
            "LL55 2SG",
            "LL57 4HG",
            "LL57 3UA",
        ]:
            return None

        return super().address_record_to_dict(record)
