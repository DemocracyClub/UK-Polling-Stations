from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "BOL"
    addresses_name = (
        "2022-05-05/2022-03-30T11:53:04.741749/Democracy_Club__05May2022.CSV"
    )
    stations_name = (
        "2022-05-05/2022-03-30T11:53:04.741749/Democracy_Club__05May2022.CSV"
    )
    elections = ["2022-05-05"]

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "100012434533",  # RATCLIFFES FARM HOUSE, WINGATES LANE, WESTHOUGHTON, BOLTON
            "10070916825",  # CURLEYS FISHERY, TOP O TH WALLSUCHES, HORWICH, BOLTON
            "100012431797",  # 321 DERBY STREET, BOLTON
            "10001244960",  # FLAT 3, 115-117 DERBY STREET, BOLTON
            "100012556511",  # 152 LONGSIGHT, BOLTON
            "10001244221",  # FLAT 1 290 ST HELENS ROAD, BOLTON
            "100010919316",
        ]:
            return None

        if record.addressline6 in [
            "BL2 4JU",
            "BL4 8JA",
            "BL1 5DB",
            "BL1 5HP",
            "BL1 3SJ",
            "BL1 2HZ",
            "BL3 2DP",
            "BL4 0LW",
            "BL5 2DL",
            "BL6 4ED",
            "BL5 2DJ",
        ]:
            return None

        rec = super().address_record_to_dict(record)

        if record.addressline6.strip() == "BL7 OHR":
            rec["postcode"] = "BL7 0HR"

        if record.addressline6.strip() == "BL4 ONX":
            rec["postcode"] = "BL4 0NX"

        if record.addressline6.strip() == "BL4 ONY":
            rec["postcode"] = "BL4 0NY"

        return rec
