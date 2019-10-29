from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "W06000004"
    addresses_name = "parl.2019-12-12/Version 1/Democracy_Club__12December2019Denb.tsv"
    stations_name = "parl.2019-12-12/Version 1/Democracy_Club__12December2019Denb.tsv"
    csv_delimiter = "\t"
    csv_encoding = "windows-1252"
    elections = ["parl.2019-12-12"]
    allow_station_point_from_postcode = False

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)

        uprn = record.property_urn.lstrip("0")

        if uprn in [
            "10023749403",  # LL210HN -> LL210HW : Bryn Ffynnon Bungalow, Corwen, Sir Ddinbych/Denbighshire
            "10091598193",  # LL184DY -> LL184QA : D 57 New Pines Caravan Park, Dyserth Road, Rhyl
            "10023752567",  # LL184DY -> LL184QJ : E 67 New Pines Caravan Park, Dyserth Road, Rhyl
            "10091598194",  # LL184DY -> LL184QA : E 82 New Pines Caravan Park, Dyserth Road, Rhyl
            "10091601258",  # LL184DY -> LL184QA : D 42 New Pines Caravan Park, Dyserth Road, Rhyl
            "200004303814",  # LL181PH -> LL181PG : Flat 2, 20 Aquarium Street, Rhyl
            "200004293591",  # CH74DE -> CH74DD : Ty Minffordd, Eryrys, Yr Wyddgrug/Mold
            "10023751330",  # LL152NL -> LL152NA : Pencoed, Clawddnewydd, Rhuthun/Ruthin
        ]:
            rec["accept_suggestion"] = True

        if uprn in [
            # Wrong postcode in addressbase
            "10093589383",  # LL170HT -> LL170TH : Dolafon Lodge, Rhyl Road, Llanelwy/St Asaph
        ]:
            rec["accept_suggestion"] = False

        return rec
