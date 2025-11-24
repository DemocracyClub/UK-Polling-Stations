import csv

from councils.models import Council
from councils.tests.factories import CouncilFactory
from django.forms import model_to_dict
from django.test import TestCase
from file_uploads.accessibility_information_handler import (
    AccessibilityInformationHandler,
)
from pollingstations.models import AccessibilityInformation, PollingStation
from pollingstations.tests.factories import (
    AccessibilityInformationFactory,
    PollingStationFactory,
)


class AccessibilityInformationHandlerTest(TestCase):
    def setUp(self):
        CouncilFactory(council_id="FOO")
        PollingStationFactory(council_id="FOO", internal_council_id="1")
        self.valid_header = [
            "internal_council_id",
            "polling_station_address",
            "polling_station_postcode",
            "polling_station_uprn",
            "polling_station_identifier",
            "is_temporary",
            "nearby_parking",
            "disabled_parking",
            "level_access",
            "temporary_ramp",
            "hearing_loop",
            "public_toilets",
            "getting_to_the_station",
            "getting_to_the_station_cy",
            "at_the_station",
            "at_the_station_cy",
        ]

    def test_handle_row(self):
        handler = AccessibilityInformationHandler(
            council=Council.objects.get(council_id="FOO")
        )
        self.assertEqual(0, AccessibilityInformation.objects.all().count())
        handler.handle_row({"is_temporary": "YES", "internal_council_id": "1"})
        self.assertEqual(1, AccessibilityInformation.objects.all().count())

    def test_handle_row_bad_id(self):
        handler = AccessibilityInformationHandler(
            council=Council.objects.get(council_id="FOO")
        )
        self.assertEqual(0, AccessibilityInformation.objects.all().count())
        handler.handle_row({"is_temporary": "YES", "internal_council_id": "2"})
        self.assertEqual(0, AccessibilityInformation.objects.all().count())
        self.assertListEqual(
            ["No polling station found with internal_council_id '2'"], handler.errors
        )

    def test_delete_existing_info(self):
        AccessibilityInformationFactory(
            polling_station=PollingStation.objects.get(
                council_id="FOO", internal_council_id="1"
            )
        )

        self.assertEqual(
            1,
            AccessibilityInformation.objects.filter(
                polling_station__council_id="FOO"
            ).count(),
        )

        handler = AccessibilityInformationHandler(
            council=Council.objects.get(council_id="FOO")
        )

        handler.delete_existing_info()
        self.assertEqual(
            0,
            AccessibilityInformation.objects.filter(
                polling_station__council_id="FOO"
            ).count(),
        )

    def test_check_valid_header(self):
        handler = AccessibilityInformationHandler(
            council=Council.objects.get(council_id="FOO")
        )

        handler.header = self.valid_header
        handler.check_header()
        self.assertListEqual([], handler.warnings)
        self.assertListEqual([], handler.errors)

    def test_check_header_field_name_changed(self):
        handler = AccessibilityInformationHandler(
            council=Council.objects.get(council_id="FOO")
        )
        header = self.valid_header
        header.remove("internal_council_id")
        header += ["polling_station_id"]
        handler.header = header
        handler.check_header()
        self.assertListEqual(
            ["Field: 'internal_council_id' missing from header"], handler.errors
        )

    def test_check_header_missing_field(self):
        handler = AccessibilityInformationHandler(
            council=Council.objects.get(council_id="FOO")
        )

        header = self.valid_header
        header.remove("nearby_parking")
        handler.header = header
        handler.check_header()
        self.assertListEqual([], handler.warnings)
        self.assertListEqual(
            ["Field: 'nearby_parking' missing from header"], handler.errors
        )

    def test_check_correct_row_lengths(self):
        handler = AccessibilityInformationHandler(
            council=Council.objects.get(council_id="FOO")
        )
        handler.header = self.valid_header

        reader = csv.reader(
            [
                """20336,"Tredegarville Primary School, Glossop Road, Adamsdown, Cardiff",CF24 0JT,200001850808,AA,No,Yes,No,Yes,,Yes,No,Instructions on how to get there from the council,Cyfarwyddiadau ar sut i gyrraedd yno gan y cyngor,What the council says you should do once you’re therer,Beth mae'r cyngor yn dweud y dylech chi ei wneud unwaith y byddwch chi yno""",
                '20340,"Little Angels Flying Start Nursery, Corner of Constellation / Metal Street, Adamsdown, Cardiff ",CF24 0LZ,100101042723,AB,No,Yes,No,No,Yes,Yes,No,,,,',
                ",,,,,,,,,,,,,,,",
            ],
        )

        handler.check_row_lengths(reader)
        self.assertListEqual([], handler.errors)

    def test_check_incorrect_row_lengths(self):
        handler = AccessibilityInformationHandler(
            council=Council.objects.get(council_id="FOO")
        )
        handler.header = self.valid_header

        reader = csv.reader(
            [
                """20336,"Tredegarville Primary School, Glossop Road, Adamsdown, Cardiff",CF24 0JT,200001850808,AA,No,Yes,No,Yes,,Yes,No,Instructions on how to get there from the council,Cyfarwyddiadau ar sut i gyrraedd yno gan y cyngor,What the council says you should do once you’re therer,Beth mae'r cyngor yn dweud y dylech chi ei wneud unwaith y byddwch chi yno""",
                '20340,"Little Angels Flying Start Nursery, Corner of Constellation / Metal Street, Adamsdown, Cardiff ",CF24 0LZ,100101042723,AB,No,Yes,No,No,Yes,Yes,',
            ],
        )

        handler.check_row_lengths(reader)
        self.assertListEqual(
            ["Wrong number of columns: Expected 16 columns on row 2 found 12"],
            handler.errors,
        )

    def test_check_all_rows_have_ids(self):
        handler = AccessibilityInformationHandler(
            council=Council.objects.get(council_id="FOO")
        )
        handler.header = self.valid_header

        reader = csv.reader(
            [
                """20336,"Tredegarville Primary School, Glossop Road, Adamsdown, Cardiff",CF24 0JT,200001850808,AA,No,Yes,No,Yes,,Yes,No,Instructions on how to get there from the council,Cyfarwyddiadau ar sut i gyrraedd yno gan y cyngor,What the council says you should do once you’re therer,Beth mae'r cyngor yn dweud y dylech chi ei wneud unwaith y byddwch chi yno""",
                '20340,"Little Angels Flying Start Nursery, Corner of Constellation / Metal Street, Adamsdown, Cardiff ",CF24 0LZ,100101042723,AB,No,Yes,No,No,Yes,Yes,No,,,,',
            ],
        )

        handler.check_all_rows_have_ids(reader)
        self.assertListEqual(
            [],
            handler.errors,
        )

    def test_check_all_rows_have_ids_header_missing_id_field(self):
        handler = AccessibilityInformationHandler(
            council=Council.objects.get(council_id="FOO")
        )
        header = self.valid_header
        header.remove("internal_council_id")
        handler.header = header
        reader = csv.reader(
            [
                """"Tredegarville Primary School, Glossop Road, Adamsdown, Cardiff",CF24 0JT,200001850808,AA,No,Yes,No,Yes,,Yes,No,Instructions on how to get there from the council,Cyfarwyddiadau ar sut i gyrraedd yno gan y cyngor,What the council says you should do once you’re therer,Beth mae'r cyngor yn dweud y dylech chi ei wneud unwaith y byddwch chi yno""",
                '"Little Angels Flying Start Nursery, Corner of Constellation / Metal Street, Adamsdown, Cardiff ",CF24 0LZ,100101042723,AB,No,Yes,No,No,Yes,Yes,No,,,,',
            ],
        )

        handler.check_all_rows_have_ids(reader)

        self.assertListEqual(
            ["Field: 'internal_council_id' missing from header"],
            handler.errors,
        )

    def test_check_all_rows_have_ids_produces_error(self):
        handler = AccessibilityInformationHandler(
            council=Council.objects.get(council_id="FOO")
        )
        handler.header = self.valid_header

        reader = csv.reader(
            [
                """20336,"Tredegarville Primary School, Glossop Road, Adamsdown, Cardiff",CF24 0JT,200001850808,AA,No,Yes,No,Yes,,Yes,No,Instructions on how to get there from the council,Cyfarwyddiadau ar sut i gyrraedd yno gan y cyngor,What the council says you should do once you’re therer,Beth mae'r cyngor yn dweud y dylech chi ei wneud unwaith y byddwch chi yno""",
                ',"Little Angels Flying Start Nursery, Corner of Constellation / Metal Street, Adamsdown, Cardiff ",CF24 0LZ,100101042723,AB,No,Yes,No,No,Yes,Yes,No,,,,',
            ],
        )

        handler.check_all_rows_have_ids(reader)
        self.assertListEqual(["Some rows missing station id"], handler.errors)

    def test_parse_data(self):
        handler = AccessibilityInformationHandler(
            council=Council.objects.get(council_id="FOO")
        )

        data = handler.parse_data(
            [
                "internal_council_id,polling_station_address,polling_station_postcode,polling_station_uprn,polling_station_identifier,is_temporary,nearby_parking,disabled_parking,level_access,temporary_ramp,hearing_loop,public_toilets,getting_to_the_station,getting_to_the_station_cy,at_the_station,at_the_station_cy",
                """20336,"Tredegarville Primary School, Glossop Road, Adamsdown, Cardiff",CF24 0JT,200001850808,AA,No,Yes,No,Yes,,Yes,No,Instructions on how to get there from the council,Cyfarwyddiadau ar sut i gyrraedd yno gan y cyngor,What the council says you should do once you’re therer,Beth mae'r cyngor yn dweud y dylech chi ei wneud unwaith y byddwch chi yno""",
                '20340,"Little Angels Flying Start Nursery, Corner of Constellation / Metal Street, Adamsdown, Cardiff ",CF24 0LZ,100101042723,AB,No,Yes,No,No,Yes,Yes,No,,,,',
            ],
        )

        self.assertIsInstance(data, csv.DictReader)
        self.assertListEqual(self.valid_header, handler.header)
        self.assertListEqual([], handler.errors)
        self.assertEqual("20336", next(data)["internal_council_id"])
        self.assertEqual("20340", next(data)["internal_council_id"])

    def test_handle_row_valid(self):
        station = PollingStationFactory(council_id="FOO", internal_council_id="20336")

        with self.assertRaises(
            PollingStation.accessibility_information.RelatedObjectDoesNotExist
        ):
            station.accessibility_information
        handler = AccessibilityInformationHandler(
            council=Council.objects.get(council_id="FOO")
        )
        row = {
            "internal_council_id": "20336",
            "polling_station_address": "Tredegarville Primary School, Glossop Road, Adamsdown, Cardiff",
            "polling_station_postcode": "CF24 0JT",
            "polling_station_uprn": "200001850808",
            "polling_station_identifier": "AA",
            "is_temporary": "No",
            "nearby_parking": "",
            "disabled_parking": "No",
            "level_access": "Yes",
            "temporary_ramp": "",
            "hearing_loop": "yes",
            "public_toilets": "No",
            "getting_to_the_station": "foo",
            "getting_to_the_station_cy": "bar",
            "at_the_station": "",
            "at_the_station_cy": "",
        }
        handler.handle_row(row)

        self.assertListEqual([], handler.warnings)
        self.assertListEqual([], handler.errors)
        station.refresh_from_db()
        accessibility_information = station.accessibility_information

        self.assertDictEqual(
            {
                "at_the_station": "",
                "at_the_station_cy": "",
                "disabled_parking": False,
                "getting_to_the_station": "foo",
                "getting_to_the_station_cy": "bar",
                "hearing_loop": True,
                "is_temporary": False,
                "level_access": True,
                "nearby_parking": None,
                "polling_station": station.pk,
                "public_toilets": False,
                "temporary_ramp": None,
            },
            {
                k: v
                for k, v in model_to_dict(
                    accessibility_information,
                    fields=self.valid_header + ["polling_station"],
                ).items()
                if k != "id"
            },
        )

    def test_handle_row_no_station(self):
        station = PollingStationFactory(
            council_id="FOO", internal_council_id="station-id"
        )

        with self.assertRaises(
            PollingStation.accessibility_information.RelatedObjectDoesNotExist
        ):
            station.accessibility_information
        handler = AccessibilityInformationHandler(
            council=Council.objects.get(council_id="FOO")
        )
        row = {
            "internal_council_id": "#####-WRONG-#####",
            "polling_station_address": "Tredegarville Primary School, Glossop Road, Adamsdown, Cardiff",
            "polling_station_postcode": "CF24 0JT",
            "polling_station_uprn": "200001850808",
            "polling_station_identifier": "AA",
            "is_temporary": "No",
            "nearby_parking": "",
            "disabled_parking": "No",
            "level_access": "Yes",
            "temporary_ramp": "",
            "hearing_loop": "yes",
            "public_toilets": "No",
            "getting_to_the_station": "foo",
            "getting_to_the_station_cy": "bar",
            "at_the_station": "",
            "at_the_station_cy": "",
        }
        handler.handle_row(row)

        self.assertEqual(0, AccessibilityInformation.objects.count())
        self.assertListEqual(
            ["No polling station found with internal_council_id '#####-WRONG-#####'"],
            handler.errors,
        )

    def test_import_accessibility_info(self):
        PollingStation.objects.all().delete()

        PollingStationFactory(council_id="FOO", internal_council_id="20336")
        PollingStationFactory(council_id="FOO", internal_council_id="20340")

        self.assertEqual(0, AccessibilityInformation.objects.count())
        handler = AccessibilityInformationHandler(
            council=Council.objects.get(council_id="FOO")
        )

        data = handler.parse_data(
            [
                "internal_council_id,polling_station_address,polling_station_postcode,polling_station_uprn,polling_station_identifier,is_temporary,nearby_parking,disabled_parking,level_access,temporary_ramp,hearing_loop,public_toilets,getting_to_the_station,getting_to_the_station_cy,at_the_station,at_the_station_cy",
                """20336,"Tredegarville Primary School, Glossop Road, Adamsdown, Cardiff",CF24 0JT,200001850808,AA,No,Yes,No,Yes,,Yes,No,Instructions on how to get there from the council,Cyfarwyddiadau ar sut i gyrraedd yno gan y cyngor,What the council says you should do once you’re therer,Beth mae'r cyngor yn dweud y dylech chi ei wneud unwaith y byddwch chi yno""",
                '20340,"Little Angels Flying Start Nursery, Corner of Constellation / Metal Street, Adamsdown, Cardiff ",CF24 0LZ,100101042723,AB,No,Yes,No,No,Yes,Yes,No,,,,',
            ],
        )

        handler.import_accessibility_info(data)

        self.assertEqual(2, AccessibilityInformation.objects.count())
        self.assertListEqual([], handler.warnings)
        self.assertListEqual([], handler.errors)

    def test_check_row_count_vs_station_count(self):
        handler = AccessibilityInformationHandler(
            council=Council.objects.get(council_id="FOO")
        )
        self.assertListEqual([], handler.warnings)
        self.assertListEqual([], handler.errors)
        handler.check_row_count_vs_station_count(3)
        self.assertListEqual(
            ["File has 3 rows, but there are 1 stations."], handler.warnings
        )
        self.assertListEqual([], handler.errors)

    def test_import_accessibility_info_duplicate_id(self):
        PollingStation.objects.all().delete()
        station = PollingStationFactory(council_id="FOO", internal_council_id="20336")
        PollingStationFactory(council_id="FOO", internal_council_id="20340")

        self.assertEqual(0, AccessibilityInformation.objects.count())
        handler = AccessibilityInformationHandler(
            council=Council.objects.get(council_id="FOO")
        )

        data = handler.parse_data(
            [
                "internal_council_id,polling_station_address,polling_station_postcode,polling_station_uprn,polling_station_identifier,is_temporary,nearby_parking,disabled_parking,level_access,temporary_ramp,hearing_loop,public_toilets,getting_to_the_station,getting_to_the_station_cy,at_the_station,at_the_station_cy",
                """20336,"Tredegarville Primary School, Glossop Road, Adamsdown, Cardiff",CF24 0JT,200001850808,AA,No,Yes,No,Yes,,Yes,No,Instructions on how to get there from the council,Cyfarwyddiadau ar sut i gyrraedd yno gan y cyngor,What the council says you should do once you’re therer,Beth mae'r cyngor yn dweud y dylech chi ei wneud unwaith y byddwch chi yno""",
                '20336,"Little Angels Flying Start Nursery, Corner of Constellation / Metal Street, Adamsdown, Cardiff ",CF24 0LZ,100101042723,AB,No,Yes,No,No,Yes,Yes,No,,,,',
            ],
        )

        handler.import_accessibility_info(data)

        self.assertEqual(1, AccessibilityInformation.objects.count())
        self.assertEqual(
            station.pk,
            AccessibilityInformation.objects.all().first().polling_station.pk,
        )
        self.assertEqual(
            ["There was more than one row containing the following ids: 20336"],
            handler.warnings,
        )
        self.assertEqual([], handler.errors)

    def test_handle(self):
        PollingStation.objects.all().delete()
        PollingStationFactory(council_id="FOO", internal_council_id="20336")
        PollingStationFactory(council_id="FOO", internal_council_id="20340")
        self.assertEqual(0, AccessibilityInformation.objects.count())
        handler = AccessibilityInformationHandler(
            council=Council.objects.get(council_id="FOO")
        )

        handler.handle(
            [
                "internal_council_id,polling_station_address,polling_station_postcode,polling_station_uprn,polling_station_identifier,is_temporary,nearby_parking,disabled_parking,level_access,temporary_ramp,hearing_loop,public_toilets,getting_to_the_station,getting_to_the_station_cy,at_the_station,at_the_station_cy",
                """20336,"Tredegarville Primary School, Glossop Road, Adamsdown, Cardiff",CF24 0JT,200001850808,AA,No,Yes,No,Yes,,Yes,No,Instructions on how to get there from the council,Cyfarwyddiadau ar sut i gyrraedd yno gan y cyngor,What the council says you should do once you’re therer,Beth mae'r cyngor yn dweud y dylech chi ei wneud unwaith y byddwch chi yno""",
                '20340,"Little Angels Flying Start Nursery, Corner of Constellation / Metal Street, Adamsdown, Cardiff ",CF24 0LZ,100101042723,AB,No,Yes,No,No,Yes,Yes,No,,,,',
            ],
        )

        self.assertEqual(2, AccessibilityInformation.objects.count())
        self.assertEqual([], handler.warnings)
        self.assertEqual([], handler.errors)
