from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "BGW"
    addresses_name = "2024-07-04/2024-06-03T14:59:22.820048/Eros_SQL_Output011.csv"
    stations_name = "2024-07-04/2024-06-03T14:59:22.820048/Eros_SQL_Output011.csv"
    elections = ["2024-07-04"]

    def station_record_to_dict(self, record):
        # The following postcode changes have been approved by the council:

        # 'SALVATION ARMY HALL, HILL STREET, ABERTILLERY, NP13 1DU' (id: 95)
        if record.pollingvenueid == "95":
            record = record._replace(pollingstationpostcode="NP13 1AL")

        # 'ST. JOSEPH'S R.C. PRIMARY SCHOOL, ASHVALE, TREDEGAR, NP22 4AQ' (id: 19)
        if record.pollingvenueid == "19":
            record = record._replace(pollingstationpostcode="NP22 3RU")

        # 'BRYNTEG YOUTH CENTRE, BRYNTEG, EBBW VALE, NP23 6ND' (id: 108)
        if record.pollingvenueid == "108":
            record = record._replace(pollingstationpostcode="NP23 6LZ")

        # 'YSTRUTH LADIES HALL, SURGERY ROAD, BLAINA, NP13 3JZ' (id: 90)
        if record.pollingvenueid == "90":
            record = record._replace(pollingstationpostcode="NP13 3AZ")

        # 'GLANHOWY PRIMARY SCHOOL (NURSERY), GLANHOWY PRIMARY SCHOOL, DUKESTOWN ROAD, TREDEGAR, NP22 4QW' (id: 74)
        if record.pollingvenueid == "74":
            record = record._replace(pollingstationpostcode="NP22 4QD")

        # The council have confirmed the following stations postcodes as correct:

        # 'CWM COMMUNITY EDUCATION & YOUTH CENTRE, CANNING STREET, CWM, EBBW VALE, NP23 7RD' (id: 86)
        # 'HOLY TRINITY & ST ANNES CHURCH, CHURCH PLACE, KING STREET, NANTYGLO, NP23 4LB' (id: 110)
        # 'TREFIL VILLAGE HALL, TREFIL, TREDEGAR, NP22 4HG' (id: 48)
        # 'ORPHEUS MUSIC CENTRE, RAWLINSON TERRACE, TREDEGAR, NP22 4LF' (id: 94)
        # # 'HILLTOP LOG CABIN, DARBY CRESCENT, HILLTOP, EBBW VALE, NP23 6QE' (id: 85)
        # # 'WILLIAM POWELL MEMORIAL HALL, BOURNVILLE ROAD, BLAINA, NP13 3ES' (id: 39)
        # # 'THE HALL, TIRZAH BAPTIST CHURCH, STATION TERRACE, CWM, EBBW VALE, NP23 6SD' (id: 77)
        # # 'CAERSALEM CHAPEL, PARK VIEW, WAUNLLWYD, EBBW VALE, NP23 6UD' (id: 49)

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "100100460975",  # 27A QUEEN STREET, NANTYGLO
            "100100460974",  # 27B QUEEN STREET, NANTYGLO
            "10014116610",  # 1 MOUNTAIN AIR, EBBW VALE
            "10014116959",  # 8 RESERVOIR ROAD, BEAUFORT, EBBW VALE
            "100101035264",  # HILL RISE, LLANGYNIDR ROAD, BEAUFORT, EBBW VALE
        ]:
            return None

        if record.housepostcode in [
            "NP23 5DH",  # split
        ]:
            return None

        return super().address_record_to_dict(record)
