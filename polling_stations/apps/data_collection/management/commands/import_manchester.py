from data_collection.management.commands import (
    BaseXpressDCCsvInconsistentPostcodesImporter,
)


class Command(BaseXpressDCCsvInconsistentPostcodesImporter):
    council_id = "E08000003"
    addresses_name = "parl.2019-12-12/Version 1/Democracy_Club__12December2019manc.tsv"
    stations_name = "parl.2019-12-12/Version 1/Democracy_Club__12December2019manc.tsv"
    elections = ["parl.2019-12-12"]
    csv_delimiter = "\t"
    csv_encoding = "windows-1252"

    def station_record_to_dict(self, record):
        if record.polling_place_id == "7394":
            # Moston Methodist Church
            record = record._replace(
                polling_place_easting="387244", polling_place_northing="401944"
            )
        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.lstrip("0")

        if record.addressline6.strip() == "WA15 8XL":
            return None

        if uprn in [
            "10014179163",  # wrong postcode; removing is fine
        ]:
            return None

        if record.addressline6.strip() == "M15 4PF":
            rec["postcode"] = "M15 4PS"
            return rec

        if (
            record.addressline1 == "Flat 1"
            and record.addressline2 == "504 Wilmslow Road"
        ):
            rec["postcode"] = "M20 2DW"

        # invalid postcodes
        if record.addressline6.strip() == "M13 OFN":
            rec["postcode"] = "M13 0FN"

        if record.addressline6.strip() == "M11 IJJ":
            rec["postcode"] = "M11 1JJ"

        if record.addressline6.strip() == "M22 OJA":
            rec["postcode"] = "M22 0JA"

        if uprn in [
            "10090238433",  # M86JX -> M84JX : Flat Over, 32 Middleton Road, Manchester
            "77190818",  # M239DD -> M239DE : Woodbine Cottage, Wythenshawe Road, Manchester
            "77135421",  # M130AQ -> M130AR : St Josephs Little Sisters of the Poor, 52 Plymouth Grove West, Manchester
            "10090239082",  # M12PE -> M12PF : Monroes, 38 London Road, Manchester
            "10012210014",  # M228BE -> M228NN : Flat 7, 3 Brookfield Gardens, Manchester
            "10012210016",  # M228BE -> M228NN : Flat 8, 3 Brookfield Gardens, Manchester
            "10012210017",  # M228BE -> M228NN : Flat 9, 3 Brookfield Gardens, Manchester
            "10012210015",  # M228BE -> M228NN : Flat 10, 3 Brookfield Gardens, Manchester
            "10070863408",  # M113LS -> M113LL : Flat 1, 2 Whitehurst Drive, Manchester
            "10070863409",  # M113LS -> M113LL : Flat 2, 2 Whitehurst Drive, Manchester
            "10070863410",  # M113LS -> M113LL : Flat 3, 2 Whitehurst Drive, Manchester
            "10070863411",  # M113LS -> M113LL : Flat 4, 2 Whitehurst Drive, Manchester
            "10070863412",  # M113LS -> M113LL : Flat 5, 2 Whitehurst Drive, Manchester
            "10070863413",  # M113LS -> M113LL : Flat 6, 2 Whitehurst Drive, Manchester
            "10070863414",  # M113LS -> M113LL : Flat 7, 2 Whitehurst Drive, Manchester
        ]:
            rec["accept_suggestion"] = True

        if uprn in [
            "77222211",  # M90RR -> M90LR : St Clares Friary, Victoria Avenue, Manchester
            "77017081",  # M98AW -> M98GT : 19 Slack Road, Manchester
            "10090241557",  # M229UH -> M114RP : Flat 2, 179 Brownley Road, Manchester
            "10090423923",  # M130XT -> M130XS : The Bungalow Manchester Grammar School, Telfer Road, Manchester
            "77203964",  # M204ND -> M203WB : Flat 1, 12 Mauldeth Road, Manchester
            "77203965",  # M204ND -> M203WB : Flat 2, 12 Mauldeth Road, Manchester
            "77203966",  # M204ND -> M203WB : Flat 3, 12 Mauldeth Road, Manchester
            "77203967",  # M204ND -> M203WB : Flat 4, 12 Mauldeth Road, Manchester
            "77203968",  # M204ND -> M203WB : Flat 5, 12 Mauldeth Road, Manchester
            "10090238181",  # M204ND -> M203WB : Flat 6, 12 Mauldeth Road, Manchester
            "77203970",  # M204ND -> M203WB : Flat 7, 12 Mauldeth Road, Manchester
            "77203971",  # M204ND -> M203WB : Flat 8, 12 Mauldeth Road, Manchester
            "77203972",  # M204ND -> M203WB : Flat 9, 12 Mauldeth Road, Manchester
            "77203973",  # M204ND -> M203WB : Flat 10, 12 Mauldeth Road, Manchester
            "77105872",  # M203LJ -> M203LB : 81A Palatine Road, Manchester
        ]:
            rec["accept_suggestion"] = False

        return rec
