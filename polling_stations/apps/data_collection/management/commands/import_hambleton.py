from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000164"
    addresses_name = "local.2019-05-02/Version 1/Democracy_Club__02May2019hamble.tsv"
    stations_name = "local.2019-05-02/Version 1/Democracy_Club__02May2019hamble.tsv"
    elections = ["local.2019-05-02"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "200003294819",  # YO613PR -> YO613PU : Hollybush Farm, Myra Bank Lane, Crayke, York
            "10008642909",  # TS95LJ -> TS95LL : Seamer Moor Bungalow Seamer Moor Farm, Seamer Moor, Seamer, Middlesbrough
            "200001927445",  # TS95LN -> TS95LL : Falklands Wynn, Holme Lane, Seamer
            "10001280326",  # TS97DA -> TS97BZ : Hazel Grove, Whorl Hill, Faceby, Middlesbrough
            "10001287245",  # DL63TE -> DL63PL : Foxton Grange, Kirby Sigston, Northallerton
            "10013390894",  # TS96QE -> TS96QD : Caravan B Stanley Grange Stud, Great Ayton, Middlesbrough
            "10001283328",  # YO612QG -> YO612QQ : Woodmans Cottage, Pilmoor, York
            "100050359857",  # DL82PD -> DL82PE : Oaklands Long Lane, Well, Bedale
            "10070732642",  # YO611ED -> YO71ED : 146A Hambleton Place, Thirsk
            "10070731545",  # YO613QG -> YO613QE : Kyle Farm, Husthwaite Road, Easingwold, York
            "200003297809",  # DL63HR -> DL63HS : Greenacre, Gold Hill Loop Road, Swainby, Northallerton
            "200003297811",  # DL63HR -> DL63HS : Longlands, Gold Gate Lane, Swainby, Northallerton
        ]:
            rec["accept_suggestion"] = True

        if uprn in [
            "10001285174",  # DL21PP -> YO72JF : The Cart Shed, Girsby Hall Farm, Girsby, Darlington
            "100050359677",  # YO73NW -> DL81EY : 3 Sycamore Drive, Sowerby, Thirsk
            "10070735117",  # YO71AS -> YO613HY : Flat Above, 97 Long Street, Thirsk
        ]:
            rec["accept_suggestion"] = False

        return rec
