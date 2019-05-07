from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000170"
    addresses_name = (
        "europarl.2019-05-23/Version 1/Democracy_Club__23May2019Ashfield.tsv"
    )

    stations_name = (
        "europarl.2019-05-23/Version 1/Democracy_Club__23May2019Ashfield.tsv"
    )

    elections = ["europarl.2019-05-23"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if uprn == "200003310492":
            rec["postcode"] = "DE554PB"
            rec["accept_suggestion"] = False

        if uprn in [
            "100031234554",  # NG177GX -> NG177HJ : 1A Oak Street, Kirkby In Ashfield, Nottingham
            "10070852165",  # NG175HS -> NG178HS : Flat 6, 5 Borders Avenue, Kirkby In Ashfield, Nottingham
            "100031241226",  # NG178JR -> NG178JT : Waverley House, The Hill, Kirkby In Ashfield, Nottingham
            "10001342248",  # NG177FU -> NG171FU : The Old Coach House, Clumber Street, Sutton In Ashfield
        ]:
            rec["accept_suggestion"] = True

        if uprn in [
            "100031229455"  # NG178AG -> NG172PA : 4 King Street, Kirkby In Ashfield, Nottingham
        ]:
            rec["accept_suggestion"] = False

        return rec
