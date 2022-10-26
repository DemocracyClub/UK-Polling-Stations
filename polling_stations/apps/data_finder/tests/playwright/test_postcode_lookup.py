import pytest
from playwright.sync_api import expect
from django.core.management import call_command
import os
from polling_stations.apps.councils.tests.factories import CouncilFactory


@pytest.fixture
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

    with open(os.devnull, "w") as f:
        call_command("loaddata", "integration_tests_addressbase.json", stdout=f)

    yield


def test_valid_station_id(
        page, live_server, setup_data
):
    page.goto(live_server.url)
    expect(page).to_have_title("Find your polling station | Where Do I Vote?")
    expect(page.locator("h1")).to_have_text("Find your polling station")
    # TODO: Find a better way of checking if element present so we don't have to repeat this code constantly
    expect(page.locator("#id_postcode")).to_have_count(1)
    page.query_selector("#id_postcode").fill("BB11BB")
    with page.expect_navigation():
        page.query_selector('#submit-postcode').click()
    expect(page).to_have_url(f"{live_server.url}/address_select/BB11BB/")
    expect(page.locator("#id_address option:has-text('2 Baz Street, Bar Town')")).not_to_be_empty()
    page.query_selector("#id_address").select_option(label="2 Baz Street, Bar Town")
    with page.expect_navigation():
        page.query_selector('#submit-address').click()
    expect(page).to_have_url(f"{live_server.url}/address/05/")
    expect(page.locator("text=Your polling station")).not_to_be_empty()
    expect(page.locator("text=walking/driving directions")).not_to_be_empty()


def test_invalid_station_id(page, live_server, setup_data):
    page.goto(live_server.url)
    expect(page).to_have_title("Find your polling station | Where Do I Vote?")
    expect(page.locator("h1")).to_have_text("Find your polling station")
    expect(page.locator("#id_postcode")).to_have_count(1)
    page.query_selector("#id_postcode").fill("BB11BB")
    with page.expect_navigation():
        page.query_selector("#submit-postcode").click()
    expect(page).to_have_url(f"{live_server.url}/address_select/BB11BB/")
    expect(
        page.locator("#id_address option:has-text('3 Baz Street, Bar Town')")
    ).not_to_be_empty()
    page.query_selector("#id_address").select_option(label="3 Baz Street, Bar Town")
    with page.expect_navigation():
        page.query_selector("#submit-address").click()
    expect(page).to_have_url(f"{live_server.url}/address/06/")
    expect(page.locator("text=Contact Foo Council")).not_to_be_empty()


def test_postcode_without_address_picker(
        page, live_server, setup_data
):
    page.goto(live_server.url)
    expect(page).to_have_title("Find your polling station | Where Do I Vote?")
    expect(page.locator("h1")).to_have_text("Find your polling station")
    expect(page.locator("#id_postcode")).to_have_count(1)
    page.query_selector("#id_postcode").fill("NP205GN")
    with page.expect_navigation():
        page.query_selector('#submit-postcode').click()
    expect(page).to_have_url(f"{live_server.url}/address/10/")
    expect(page.locator("text=Your polling station")).not_to_be_empty()
    expect(page.locator("text=walking/driving directions")).not_to_be_empty()


def test_my_address_not_in_list(page, live_server, setup_data):
    page.goto(live_server.url)
    expect(page).to_have_title("Find your polling station | Where Do I Vote?")
    expect(page.locator("h1")).to_have_text("Find your polling station")
    expect(page.locator("#id_postcode")).to_have_count(1)
    page.query_selector("#id_postcode").fill("BB11BB")
    with page.expect_navigation():
        page.query_selector("#submit-postcode").click()
    expect(
        page.locator("#id_address option:has-text('My address is not in the list')")
    ).not_to_be_empty()
    page.query_selector("#id_address").select_option(
        label="My address is not in the list"
    )
    with page.expect_navigation():
        page.query_selector("#submit-address").click()
    expect(page).to_have_url(f"{live_server.url}/we_dont_know/BB11BB/")
    expect(page.locator("text=Contact Foo Council")).not_to_be_empty()


def test_invalid_postcode(page, live_server, setup_data):
    page.goto(f"{live_server.url}/postcode/foo")
    expect(
        page.locator("text=This doesn't appear to be a valid postcode.")
    ).not_to_be_empty()


def test_northern_ireland(page, live_server, setup_data):
    page.goto(live_server.url)
    expect(page).to_have_title("Find your polling station | Where Do I Vote?")
    expect(page.locator("h1")).to_have_text("Find your polling station")
    expect(page.locator("#id_postcode")).to_have_count(1)
    page.query_selector("#id_postcode").fill("BT15 3JX")
    with page.expect_navigation():
        page.query_selector("#submit-postcode").click()
    expect(page.locator("text=The Electoral Office for Northern Ireland")).not_to_be_empty()
    expect(page.locator("text=You will need photographic identification")).not_to_be_empty()
