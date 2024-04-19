from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "GWN"
    addresses_name = "2024-05-02/2024-04-23T11:09:58.311554/Eros_SQL_Output001.csv"
    stations_name = "2024-05-02/2024-04-23T11:09:58.311554/Eros_SQL_Output001.csv"
    elections = ["2024-05-02"]
    csv_encoding = "windows-1252"

    # > WARNING: Polling station NEUADD BENTREF ABERANGELL (0-neuadd-bentref-aberangell)
    # > is in Powys County Council (POW) but target council is Gwynedd Council (GWN) -
    # > manual check recommended
    #
    # Checked; actual village hall is within Aberangell, on the right side of the
    # boundary.

    def station_record_to_dict(self, record):
        # CAPEL HOREB - Gorsaf Newydd/New Polling Station, RHOSTRYFAN, CAERNARFON, GWYNEDD
        if record.pollingstationnumber == "22":
            # Via UPRN 10070271330 (not necessarily the same building, but close enough)
            record = record._replace(pollingstationpostcode="LL54 7LT")  # was LL57 7LT

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
        ]:
            return None

        if record.housepostcode in [
            # splits
            "LL53 5AG",
            "LL53 7TP",
            "LL53 5TP",
            "LL57 4HG",
            "LL55 2SG",
            "LL48 6AY",
            "LL54 7UB",
            "LL55 2TD",
            "LL57 3UA",
            "LL53 8DR",
            "LL53 6SY",
        ]:
            return None

        return super().address_record_to_dict(record)
