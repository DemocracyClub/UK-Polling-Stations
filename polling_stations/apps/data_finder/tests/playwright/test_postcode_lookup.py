import pytest
from context_managers import check_for_console_errors
from playwright.sync_api import expect


@pytest.mark.vcr()
def test_valid_station_id(page, live_server):
    with check_for_console_errors(page):
        page.goto(live_server.url)
        expect(page).to_have_title("Find your polling station | Where Do I Vote?")
        expect(page.locator("h1")).to_have_text("Find your polling station")
        expect(page.locator("#id_postcode")).to_have_count(1)
        page.query_selector("#id_postcode").fill("BB11BB")

        with page.expect_navigation():
            page.query_selector("#submit-postcode").click()
        expect(page).to_have_url(f"{live_server.url}/address_select/BB11BB/")
        expect(
            page.locator("#id_address option:has-text('2 Baz Street, Bar Town')")
        ).not_to_be_empty()
        page.query_selector("#id_address").select_option(label="2 Baz Street, Bar Town")

        with page.expect_navigation():
            page.query_selector("#submit-address").click()
        expect(page).to_have_url(f"{live_server.url}/address/05/")
        expect(page.locator('h2:has-text("Your polling station")')).not_to_be_empty()
        expect(page.locator("text=walking/driving directions")).not_to_be_empty()


def test_invalid_station_id(page, live_server):
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


@pytest.mark.vcr()
def test_postcode_without_address_picker(page, live_server):
    with check_for_console_errors(page):
        page.goto(live_server.url)
        expect(page).to_have_title("Find your polling station | Where Do I Vote?")
        expect(page.locator("h1")).to_have_text("Find your polling station")
        expect(page.locator("#id_postcode")).to_have_count(1)
        page.query_selector("#id_postcode").fill("NP205GN")

        with page.expect_navigation():
            page.query_selector("#submit-postcode").click()
        expect(page).to_have_url(f"{live_server.url}/address/10/")
        expect(page.locator('h2:has-text("Your polling station")')).not_to_be_empty()
        expect(page.locator("text=walking/driving directions")).not_to_be_empty()


def test_my_address_not_in_list(page, live_server):
    with check_for_console_errors(page):
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


def test_invalid_postcode(page, live_server):
    with check_for_console_errors(page):
        page.goto(f"{live_server.url}/postcode/foo")
        expect(
            page.locator("text=This doesn't appear to be a valid postcode.")
        ).not_to_be_empty()


@pytest.mark.vcr()
def test_northern_ireland(page, live_server):
    with check_for_console_errors(page):
        page.goto(live_server.url)
        expect(page).to_have_title("Find your polling station | Where Do I Vote?")
        expect(page.locator("h1")).to_have_text("Find your polling station")
        expect(page.locator("#id_postcode")).to_have_count(1)
        page.query_selector("#id_postcode").fill("BT15 3JX")

        with page.expect_navigation():
            page.query_selector("#submit-postcode").click()
        expect(
            page.locator("text=The Electoral Office for Northern Ireland")
        ).not_to_be_empty()
        expect(
            page.locator(
                "text=You will need to take photo ID to vote at a polling station in this election"
            )
        )
