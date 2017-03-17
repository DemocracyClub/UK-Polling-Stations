# -*- coding: utf-8 -*-
import os
import re
import json
from contextlib import contextmanager
from django.template.defaultfilters import slugify

from lxml import html

from django.test.client import Client
from django.core.urlresolvers import reverse
from django.core.management import call_command

from aloe import before, after, around, step, world
from aloe_django import django_url
import aloe_webdriver.django
from selenium import webdriver
import vcr

selenium_vcr = vcr.VCR()
# We need to ignore localhost as selenium communicates over local http
# to interact with the 'browser'
selenium_vcr.ignore_localhost = True

@before.each_example
def setup(scenario, outline, steps):
    # TODO Set browser in django.conf.settings
    # world.browser = webdriver.Chrome()
    world.browser = webdriver.PhantomJS()

    with open(os.devnull, "w") as f:
        call_command('loaddata', 'test_routing.json', stdout=f)
        call_command('loaddata', 'newport_council.json', stdout=f)
        call_command('loaddata', 'polling_stations/apps/data_finder/fixtures/northern_ireland.json', stdout=f)

@step('No errors were thrown')
def no_errors(step):
    assert\
        len(world.browser.get_log('browser')) == 0,\
        "JavaScript errors were logged:\n %s" %\
        (world.browser.get_log('browser'))

@after.each_example
def take_down(scenario, outline, steps):
    world.browser.quit()

@around.each_step
@contextmanager
def mock_mapit(step):
    feature = slugify(step.feature.text)
    scenario = slugify(step.scenario.text)
    step_slug = slugify(step.text)
    path = 'test_data/vcr_cassettes/integration_tests/{}/{}/{}.yaml'
    with selenium_vcr.use_cassette(path.format(feature, scenario, step_slug)):
        yield
