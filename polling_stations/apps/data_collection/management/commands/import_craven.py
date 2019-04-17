from data_collection.management.commands import (
    BaseXpressDCCsvInconsistentPostcodesImporter,
)


class Command(BaseXpressDCCsvInconsistentPostcodesImporter):
    council_id = "E07000163"
    addresses_name = "local.2019-05-02/Version 2/polling station coordinates Craven.csv"
    stations_name = "local.2019-05-02/Version 2/polling station coordinates Craven.csv"
    elections = ["local.2019-05-02"]
    csv_delimiter = ","


def address_record_to_dict(self, record):
    rec = super().address_record_to_dict(record)
    uprn = record.property_urn.strip().lstrip("0")

    if uprn in [
        "100050352517",  # BD233RB -> BD231JZ : 26 High Street, Gargrave, Skipton
        "10092993238",  # BD207RH -> BD207AR : 1 Prospect Street, Crosshills, Keighley
        "10007564837",  # LA27DQ -> LA27DH : Bowker House Farm, Mewith Lane, Bentham, Lancaster
    ]:
        rec["accept_suggestion"] = True

    if uprn in [
        "10013144569",  # BD236RD -> BD231FL : The Flat, 1 Main Street, Embsay, Skipton
        "10013144322",  # BD233LP -> BD236NF : Heber Cottage, East Marton, Skipton
        "10013146501",  # LA28PR -> LA27DH : Mearbeck Farmhouse, White Pit Lane, Tatham, Wray, Lancaster
        "10013148994",  # BD232EW -> BD233EW : 1 Carletonside Fold, Skipton
    ]:
        rec["accept_suggestion"] = False

    return rec
