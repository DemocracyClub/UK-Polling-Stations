from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "ASF"
    addresses_name = (
        "2024-05-02/2024-03-07T15:29:47.505297/Democracy_Club__02May2024.tsv"
    )
    stations_name = (
        "2024-05-02/2024-03-07T15:29:47.505297/Democracy_Club__02May2024.tsv"
    )
    elections = ["2024-05-02"]
    csv_delimiter = "\t"

    # Below warnings checked and no correction needed:
    # WARNING: Polling station Evington Hall (11939) is in Folkestone & Hythe District Council (SHE)

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "200004389187",  # MOBILE HOME AT CLOVER FARM THE PINNOCK, PLUCKLEY
            "10012873869",  # 1B BOND ROAD, ASHFORD
            "100060797854",  # KNOLLYS COTTAGE, SANDY LANE, WILLESBOROUGH, ASHFORD
            "100062379318",  # THE OLD FARMHOUSE, FAVERSHAM ROAD, THROWLEY, FAVERSHAM
        ]:
            return None

        if record.addressline6 in [
            # splits
            "TN24 9FA",
            "TN25 7AS",
        ]:
            return None

        return super().address_record_to_dict(record)
