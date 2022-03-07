from django.contrib.gis.geos import Point

from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "POR"
    addresses_name = (
        "2022-05-05/2022-03-07T11:47:50.740409/Democracy_Club__05May2022.tsv"
    )
    stations_name = (
        "2022-05-05/2022-03-07T11:47:50.740409/Democracy_Club__05May2022.tsv"
    )
    elections = ["2022-05-05"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):
        # Council thinks postcodes are correct as is for:
        # Portsmouth Methodist Church (Eastney), Highland Road, Southsea, PO4 9NJ
        # Moorings Way Infant School, Moorings Way, Southsea, PO4 8YJ
        # Christ Church, London Road, Widley, Portsmouth, PO6 3NA

        # 'Cathedral House (Becket Hall), St Thomas`s Street, Portsmouth, PO1 2HH' (id: 5282)
        if record.polling_place_id == "5282":
            record = record._replace(polling_place_postcode="PO1 2EZ")
        # 'King's Church, Somers Road, Southsea, PO5 1EE' (id: 5294)
        if record.polling_place_id == "5294":
            record = record._replace(polling_place_postcode="PO5 4QA")
        # 'Francis Lodge, Fernhurst Junior School, Heidelberg Road, Southsea, PO4 0AG' (id: 5314)
        if record.polling_place_id == "5314":
            record = record._replace(polling_place_postcode="PO4 0AP")
        # 'St Margaret's Parish Centre, Highland Road, Southsea, PO4 8AY' (id: 5322)
        if record.polling_place_id == "5322":
            record = record._replace(polling_place_postcode="PO4 9DD")
        # 'Hillside and Wymering Centre, Cheltenham Road, Portsmouth, PO6 3QY' (id: 5466)
        if record.polling_place_id == "5466":
            record = record._replace(polling_place_postcode="PO6 3PY")

        rec = super().station_record_to_dict(record)

        # St Margaret's Parish Centre
        if rec["internal_council_id"] == "5322":
            rec["location"] = Point(-1.067090, 50.786643, srid=4326)

        return rec
