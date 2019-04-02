from data_collection.management.commands import (
    BaseXpressDCCsvInconsistentPostcodesImporter,
)


class Command(BaseXpressDCCsvInconsistentPostcodesImporter):
    council_id = "E06000033"
    addresses_name = "local.2019-05-02/Version 1/Southend-on-Sea XpressDC.csv"
    stations_name = "local.2019-05-02/Version 1/Southend-on-Sea XpressDC.csv"
    elections = ["local.2019-05-02"]

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "100090684611",  # SS26UY -> SS26UH : Flat above, 281 Eastwoodbury Lane, Southend-on-Sea, Essex
            "100090667560",  # SS93NQ -> SS92AH : 1174 London Road, Leigh-on-Sea, Essex
        ]:
            rec["accept_suggestion"] = True

        if uprn in [
            "10012152101",  # SS07TA -> SS07SD : Flat 4, 31 Palmerston Road, Westcliff-on-Sea, Essex
            "10024162959",  # SS24XA -> SS24UZ : Thorpe Bay High School House, Southchurch Boulevard, Southend-on-Sea, Essex
            "100090662005",  # SS94RP -> SS94RY : 124 Eastwood Old Road, Leigh-on-Sea, Essex
            "100091605320",  # SS94RP -> SS94RY : Flat Above, 112 Eastwood Old Road, Leigh-on-Sea, Essex
            "100090662492",  # SS94LR -> SS94LT : 297 Eastwood Road North, Leigh-on-Sea, Essex
            "100090671177",  # SS92HE -> SS92HW : 99 Rectory Grove, Leigh-on-Sea, Essex
            "100091283942",  # SS91NH -> SS91NJ : 32 Chalkwell Park Drive, Leigh-on-Sea, Essex
            "10024286458",  # SS08LL -> SS08LR : 12A The Vestry, Kings Road, Westcliff-on-Sea, Essex
            "200001252210",  # SS07JZ -> SS07JY : 65A St. John`s Road, Westcliff-on-Sea, Essex
            "100090690997",  # SS39DB -> SS39PH : 43 Flat above, Ness Road, Shoeburyness, Southend-on-Sea, Essex
            "100090691012",  # SS39PH -> SS39DG : 68 Ness Road, Shoeburyness, Southend-on-Sea, Essex
            "100091581635",  # SS00AA -> SS09UN : 77B Southbourne Grove, Westcliff-on-Sea, Essex
            "100091291176",  # SS12RG -> SS12FJ : 18 Wesley Court, Southchurch Avenue, Southend-on-Sea, Essex
        ]:
            rec["accept_suggestion"] = False

        if uprn in ["10024288188", "10024288190", "10024288189"]:
            rec["accept_suggestion"] = False

        return rec
