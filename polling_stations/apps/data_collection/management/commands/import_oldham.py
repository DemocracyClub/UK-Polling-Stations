from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E08000004"
    addresses_name = "local.2019-05-02/Version 1/oldham.gov.uk-1555340067000-.tsv"
    stations_name = "local.2019-05-02/Version 1/oldham.gov.uk-1555340067000-.tsv"
    elections = ["local.2019-05-02"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if record.addressline6.strip() == "M35 09D":
            rec["postcode"] = "M35 0PD"

        if uprn in [
            "422000076707",  # OL83LB -> OL45LN : Hawthorne Inn, 365 Roundthorn Road, Oldham
            "100012737571",  # OL35QL -> OL35AG : Ladbrook, Sandy Lane, Dobcross
        ]:
            rec["accept_suggestion"] = True

        if uprn in [
            "422000111697",  # OL45SN -> OL35SP : 150 Oldham Road, Springhead
            "422000111695",  # OL45SN -> OL35SP : 146 Oldham Road, Springhead
            "422000111696",  # OL45SN -> OL35SP : 148 Oldham Road, Springhead
            "422000034208",  # M359JN -> M359JR : 69 Church Street, Failsworth
            "422000126515",  # OL43FS -> OL43QA : 1 Old Manor Farm Close, Oldham
        ]:
            rec["accept_suggestion"] = False

        return rec
