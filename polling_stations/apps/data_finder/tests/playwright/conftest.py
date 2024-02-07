import datetime
import os

import pytest
from data_importers.event_types import DataEventType
from data_importers.tests.factories import DataEventFactory
from django.core.management import call_command
from django.utils import timezone

from polling_stations.apps.councils.tests.factories import CouncilFactory


@pytest.fixture(autouse=True)
def setup_data():
    CouncilFactory(
        **{
            "council_id": "NWP",
            "electoral_services_address": "Newport City Council\nCivic Centre\nNewport\nSouth Wales",
            "electoral_services_email": "uvote@newport.gov.uk",
            "electoral_services_phone_numbers": ["01633 656656"],
            "electoral_services_postcode": "NP20 4UR",
            "electoral_services_website": "http://www.newport.gov.uk/_dc/index.cfm?fuseaction=electoral.homepage",
            "name": "Newport Council",
            "identifiers": ["W06000022"],
        }
    )
    CouncilFactory(
        **{
            "council_id": "FOO",
            "name": "Foo Council",
            "electoral_services_email": "",
            "electoral_services_phone_numbers": [""],
            "electoral_services_website": "",
            "electoral_services_postcode": "",
            "electoral_services_address": "",
            "identifiers": ["X01"],
        }
    )
    CouncilFactory(
        **{
            "council_id": "BST",
            "name": "Bristol City Council",
            "electoral_services_email": "",
            "electoral_services_phone_numbers": [""],
            "electoral_services_website": "",
            "electoral_services_postcode": "",
            "electoral_services_address": "",
            "identifiers": ["E06000023"],
        }
    )
    CouncilFactory(
        **{
            "council_id": "BFD",
            "name": "",
            "electoral_services_email": "info@eoni.org.uk",
            "electoral_services_phone_numbers": [""],
            "electoral_services_website": "http://www.eoni.org.uk/",
            "electoral_services_postcode": "",
            "electoral_services_address": "",
            "identifiers": ["N09000003"],
        }
    )
    DataEventFactory(
        council_id="FOO",
        event_type=DataEventType.IMPORT,
        election_dates=[timezone.now().date() + datetime.timedelta(days=1)],
    )
    DataEventFactory(
        council_id="NWP",
        event_type=DataEventType.IMPORT,
        election_dates=[timezone.now().date() + datetime.timedelta(days=1)],
    )

    with open(os.devnull, "w") as f:
        call_command("loaddata", "integration_tests_addressbase.json", stdout=f)

    yield
