from data_collection.management.commands import BaseXpressWebLookupCsvImporter


class Command(BaseXpressWebLookupCsvImporter):
    council_id = "W06000004"
    addresses_name = "PropertyPostCodePollingStationWebLookup-2016-02-09.CSV"
    stations_name = "PropertyPostCodePollingStationWebLookup-2016-02-09.CSV"
    csv_encoding = "latin-1"
    station_id_field = "pollingdistrictreference"
    elections = ["local.denbighshire.2017-05-04", "parl.2017-06-08"]

    """
    Joe received following reply from Denbighshire council:

    Same data as for 2016, except for...

    BLA
    UPRN                    10023752725

    St Asaph City Council Meeting Room
    Roe Park Meadow
    High Street
    St Asaph, LL17 0RD


    BLB
    UPRN                    200004301587

    St Asaph Cricket Club Pavilion
    The Roe
    St Asaph
    LL17 0LU

    .. so we will import last year's file and manually bodge in the changes
    """

    def station_record_to_dict(self, record):
        district_id = getattr(record, self.station_id_field).strip()

        if district_id == "BLA":
            record = record._replace(
                pollingplaceaddress1="St Asaph City Council Meeting Room"
            )
            record = record._replace(pollingplaceaddress2="Roe Park Meadow")
            record = record._replace(pollingplaceaddress3="High Street")
            record = record._replace(pollingplaceaddress4="St Asaph")
            record = record._replace(pollingplaceaddress5="")
            record = record._replace(pollingplaceaddress6="")
            record = record._replace(pollingplaceaddress7="LL17 0RD")
            record = record._replace(pollingplaceeasting="0")
            record = record._replace(pollingplacenorthing="0")
        if district_id == "BLB":
            record = record._replace(
                pollingplaceaddress1="St Asaph Cricket Club Pavilion"
            )
            record = record._replace(pollingplaceaddress2="The Roe")
            record = record._replace(pollingplaceaddress3="St Asaph")
            record = record._replace(pollingplaceaddress4="")
            record = record._replace(pollingplaceaddress5="")
            record = record._replace(pollingplaceaddress6="")
            record = record._replace(pollingplaceaddress7="LL17 0LU")
            record = record._replace(pollingplaceeasting="0")
            record = record._replace(pollingplacenorthing="0")

        address = self.get_station_address(record)
        location = self.get_station_point(record)
        return {
            "internal_council_id": district_id,
            "postcode": getattr(record, self.station_postcode_field).strip(),
            "address": address.strip(),
            "location": location,
        }
