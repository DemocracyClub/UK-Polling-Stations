from django.core.exceptions import ObjectDoesNotExist
from data_collection.base_importers import BaseStationsAddressesImporter
from addressbase.models import Address


class Command(BaseStationsAddressesImporter):
    srid = 27700
    districts_srid = 27700
    stations_filetype = 'shp'
    addresses_filetype = 'shp'
    council_id = 'E07000151'
    addresses_name = 'UPRN_PollingStationRef.shp'
    stations_name = 'DDC Polling Stations.shp'
    elections = ['local.northamptonshire.2017-05-04']

    def address_record_to_dict(self, record):
        try:
            address = Address.objects.get(pk=record.record[1])
        except ObjectDoesNotExist:
            return None

        return {
            'address': address.address,
            'postcode': address.postcode,
            'polling_station_id': record.record[0],
        }

    def format_address(self, record):
        address_parts = [record[x].strip() for x in range(3, 7)]
        for i, part in enumerate(address_parts):
            if part == b'':
                address_parts[i] = ''
        address = "\n".join(address_parts)
        while "\n\n" in address:
            address = address.replace("\n\n", "\n")
        return address.strip()

    def station_record_to_dict(self, record):
        codes = record[1].split(',')

        # Joe received corrections by email from Daventry:
        # Welford Polling Station – FM (Sulby) and Welford (GA)
        # AC is Althorp Polling District, but they vote at
        # Harlestone Village Institute (Polling Station ID 67)
        if record[0] == 66:
            codes = ['FM', 'GA']
        if record[0] == 67:
            codes.append('AC')

        codes = [code.strip() for code in codes]

        stations = []
        for code in codes:
            stations.append({
                'internal_council_id': code,
                'postcode': record[8].strip(),
                'address': self.format_address(record),
            })
        return stations
