from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E06000003"
    addresses_name = (
        "parl.2019-12-12/Version 1/Democracy_Club__12December2019redcar.tsv"
    )
    stations_name = "parl.2019-12-12/Version 1/Democracy_Club__12December2019redcar.tsv"
    elections = ["parl.2019-12-12"]
    csv_delimiter = "\t"
    allow_station_point_from_postcode = False

    def station_record_to_dict(self, record):
        if (
            record.polling_place_id == "15380"
            and record.polling_place_postcode == "TS12 2EE"
        ):
            # Skelton Civic Centre, Coniston Road (wrong postcode)
            record = record._replace(polling_place_postcode="TS12 2HP")
        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10034518861",  # TS79ND -> TS79LF : Centurion Inn, Allendale Road, Ormesby
            "100110675731",  # TS134DG -> TS134EA : Garth Holme, Brotton Road, Carlin How
            "200002523561",  # TS70JU -> TS70PF : 2 Haselea Morton Carr Crossing, Nunthorpe, Middlesbrough
            "10023902772",  # TS122EA -> TS122BG : 1 Oak Mews, The Hills, Skelton-in-Cleveland, Saltburn by the Sea
            "10023902773",  # TS122EA -> TS122BG : 2 Oak Mews, The Hills, Skelton-in-Cleveland, Saltburn by the Sea
            "200002523768",  # TS122HD -> TS122HE : The Mill, Marske Lane, Skelton-in-Cleveland, Saltburn by the Sea
            "200002523076",  # TS122BG -> TS122BH : Rosemont, Swilly Lane, Skelton-in-Cleveland, Saltburn by the Sea
            "100110776824",  # TS121JG -> TS121HA : Toll Bridge Cottage, Saltburn Lane, Saltburn by the Sea
            "100110676493",  # TS122JT -> TS121HA : White House Lodge, Saltburn Lane, Skelton-in-Cleveland
        ]:
            rec["accept_suggestion"] = True
        #
        if uprn in [
            "100110675105",  # TS101RP -> TS101SS : 51 Cherry Trees, Coatham Road, Redcar
            "100110056129",  # TS60PA -> TS60NX : 56 South Park Avenue, Normanby
            "10023907833",  # TS146BN -> TS146HG : Nes-Ley Rear Of 7 Market Place, Westgate, Guisborough
            "10023901711",  # TS116BF -> TS68DN : 2 Rosedene Mews, Redcar Road, Marske by the Sea, Redcar
            "10023903438",  # TS121AT -> TS121AU : Windsor Hall, Windsor Road, Saltburn by the Sea
            # Looks like the wrong postcode in AddressBase
            "10034529574",
            "200002524170",
        ]:
            rec["accept_suggestion"] = False

        return rec
