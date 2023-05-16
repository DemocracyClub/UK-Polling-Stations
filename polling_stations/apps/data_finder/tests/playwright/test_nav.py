from context_managers import check_for_console_errors
from playwright.sync_api import expect


def test_api(page, live_server):
    with check_for_console_errors(page):
        page.goto(f"{live_server.url}/api")
        expect(page.locator("text=wheredoivote.co.uk Beta API")).not_to_be_empty()


def test_api_beta(page, live_server):
    with check_for_console_errors(page):
        page.goto(f"{live_server.url}/api/beta")
        expect(page.locator("h1")).to_have_text("Api Root")


def test_feedback(page, live_server):
    with check_for_console_errors(page):
        page.goto(f"{live_server.url}/feedback")
        expect(page.locator("text=Did you find this useful?"))


def test_report_problem(page, live_server):
    with check_for_console_errors(page):
        page.goto(f"{live_server.url}/report_problem")
        expect(page.locator("h3")).to_have_text("Report a Problem")


def test_embed(page, live_server):
    with check_for_console_errors(page):
        page.goto(f"{live_server.url}/embed")
        expect(page.locator("text=Enter your postcode")).not_to_be_empty()


def test_example(page, live_server):
    with check_for_console_errors(page):
        page.goto(f"{live_server.url}/example")
        expect(page.locator("h2")).to_have_text("Your polling station")
