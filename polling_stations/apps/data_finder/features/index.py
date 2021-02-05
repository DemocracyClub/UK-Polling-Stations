# -*- coding: utf-8 -*-
import re
import os
import shutil
import signal
import tempfile
from contextlib import contextmanager
from django.template.defaultfilters import slugify
from django.conf import settings
from django.core.management import call_command
from aloe import before, after, around, step, world
import aloe_webdriver.django  # noqa
from selenium.webdriver import Chrome, ChromeOptions
import vcr

from councils.tests.factories import CouncilFactory

selenium_vcr = vcr.VCR()
# We need to ignore localhost as selenium communicates over local http
# to interact with the 'browser'
selenium_vcr.ignore_localhost = True

temp_dir = tempfile.mkdtemp()


@before.all
def before_all():
    # build static assets into a temporary location
    settings.STATIC_ROOT = temp_dir
    call_command("collectstatic", interactive=False, verbosity=0)


@after.all
def after_all():
    # clean up static assets
    shutil.rmtree(temp_dir)


@before.each_example
def setup(scenario, outline, steps):
    options = ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_experimental_option("w3c", False)
    world.browser = Chrome(options=options)
    world.browser.set_page_load_timeout(10)
    world.browser.set_script_timeout(10)

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
        # call_command("loaddata", "newport_council.json", stdout=f)
        call_command("loaddata", "integration_tests_addressbase.json", stdout=f)


@step("No errors were thrown")
def no_errors(step):
    assert (
        len(world.browser.get_log("browser")) == 0
    ), "JavaScript errors were logged:\n %s" % (world.browser.get_log("browser"))


@after.each_example
def take_down(scenario, outline, steps):
    try:
        # we can do this the easy way...
        world.browser.quit()
    except OSError:
        # ..or we can do this the hard way
        world.browser.service.process.send_signal(signal.SIGTERM)


@before.each_step
def each_step(step):
    print(str(step))


@around.each_step
@contextmanager
def mock_http_calls(step):
    feature = slugify(step.feature.text)
    scenario = slugify(step.scenario.text)
    step_slug = slugify(re.sub(r"localhost:(\d+)/", "localhost/", step.text))
    path = "test_data/vcr_cassettes/integration_tests/{}/{}/{}.yaml"
    with selenium_vcr.use_cassette(path.format(feature, scenario, step_slug)):
        yield
