from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000164"
    addresses_name = "parl.2019-12-12/Version 1/merged.tsv"
    stations_name = "parl.2019-12-12/Version 1/merged.tsv"
    elections = ["parl.2019-12-12"]
    csv_delimiter = "\t"
    allow_station_point_from_postcode = False

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10001280326",  # TS97DA -> TS97BZ : Hazel Grove, Whorl Hill, Faceby, Middlesbrough
            "10001283328",  # YO612QG -> YO612QQ : Woodmans Cottage, Pilmoor, York
            "10001287245",  # DL63TE -> DL63PL : Foxton Grange, Kirby Sigston, Northallerton
            "100050359857",  # DL82PD -> DL82PE : Oaklands Long Lane, Well, Bedale
            "10008642909",  # TS95LJ -> TS95LL : Seamer Moor Bungalow Seamer Moor Farm, Seamer Moor, Seamer, Middlesbrough
            "10013390894",  # TS96QE -> TS96QD : Caravan B Stanley Grange Stud, Great Ayton, Middlesbrough
            "10070731545",  # YO613QG -> YO613QE : Kyle Farm, Husthwaite Road, Easingwold, York
            "200001927445",  # TS95LN -> TS95LL : Falklands Wynn, Holme Lane, Seamer
            "200003294819",  # YO613PR -> YO613PU : Hollybush Farm, Myra Bank Lane, Crayke, York
            "200003297809",  # DL63HR -> DL63HS : Greenacre, Gold Hill Loop Road, Swainby, Northallerton
            "200003297811",  # DL63HR -> DL63HS : Longlands, Gold Gate Lane, Swainby, Northallerton
        ]:
            rec["accept_suggestion"] = True

        if uprn in [
            "10070735117",  # YO71AS -> YO613HY : Flat Above, 97 Long Street, Thirsk
        ]:
            rec["accept_suggestion"] = False

        return rec
