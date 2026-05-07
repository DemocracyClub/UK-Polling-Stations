from data_importers.management.commands import BaseHalarose2026UpdateCsvImporter


class Command(BaseHalarose2026UpdateCsvImporter):
    council_id = "GWN"
    addresses_name = "2026-05-07/2026-02-23T11:40:14.920142/GWN_combined.csv"
    stations_name = "2026-05-07/2026-02-23T11:40:14.920142/GWN_combined.csv"
    elections = ["2026-05-07"]

    def station_record_to_dict(self, record):
        # station change from council:
        # OLD: PENCADLYS Y SGOWTIAID/SCOUTS H.Q., MAES CADNANT, CAERNARFON CAERNARFON, LL55 1BS
        # NEW: Ganolfan Hamdden Arfon Leisure Centre, Bethel Rd, Caernarfon LL55 1HW
        if (
            self.get_station_hash(record)
            == "15-pencadlys-y-sgowtiaidscouts-hq-maes-cadnant-caernarfon"
        ):
            record = record._replace(
                pollingstationname="Ganolfan Hamdden Arfon Leisure Centre",
                pollingstationaddress1="Bethel Rd",
                pollingstationaddress2="Caernarfon",
                pollingstationpostcode="LL55 1HW",
                pollingvenueeasting="0",
                pollingvenuenorthing="0",
            )

        # bug report: https://app.asana.com/1/1204880536137786/project/1207538772343223/task/1214603910201691?focus=true
        # removing bad coordinates for:
        # Y GANOLFAN RHEOLAETH/ THE MANAGEMENT CENTRE STRYD Y COLEG/ COLLEGE ROAD BANGOR
        if (
            self.get_station_hash(record)
            == "6-y-ganolfan-rheolaeth-the-management-centre"
        ):
            record = record._replace(
                pollingvenueeasting="257876",
                pollingvenuenorthing="372501",
            )
        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "200003162781",  # 6 CHURCH PLACE, PWLLHELI
            "200003166018",  # 5 HOLYWELL TERRACE, CRICCIETH
            "200003163977",  # 19 VICTORIA ROAD, PENYGROES, CAERNARFON
            "200003165113",  # 4 POOL HILL, CAERNARFON
            "10090569131",  # FLAT 21 POOL STREET, CAERNARFON
            "200003164854",  # 23 POOL HILL, CAERNARFON
            "200003164853",  # 21 POOL HILL, CAERNARFON
            "10070361201",  # TY CAM, RHOSTRYFAN, CAERNARFON
            "200003178611",  # COED MAWR COTTAGE, LLANBERIS ROAD, RHOSBODRUAL, CAERNARFON
            "200003178515",  # 27 LLANBERIS ROAD, RHOSBODRUAL, CAERNARFON
            "10094363547",  # 47 PLAS Y COED, BANGOR
            "200003195096",  # 8 PEN Y GRAIG, BETHESDA, BANGOR
        ]:
            return None

        if record.postcode in [
            # splits
            "LL53 5AG",
            "LL53 7TP",
            "LL48 6AY",
            "LL54 7UB",
            "LL55 2SG",
            "LL54 7BN",
            "LL53 6SY",
            "LL55 2TD",
            "LL53 8DR",
            "LL57 3UA",
        ]:
            return None

        # station change from council:
        # OLD: PENCADLYS Y SGOWTIAID/SCOUTS H.Q., MAES CADNANT, CAERNARFON CAERNARFON, LL55 1BS
        # NEW: Ganolfan Hamdden Arfon Leisure Centre, Bethel Rd, Caernarfon LL55 1HW
        if (
            self.get_station_hash(record)
            == "15-pencadlys-y-sgowtiaidscouts-hq-maes-cadnant-caernarfon"
        ):
            record = record._replace(
                pollingstationname="Ganolfan Hamdden Arfon Leisure Centre",
            )
        return super().address_record_to_dict(record)
